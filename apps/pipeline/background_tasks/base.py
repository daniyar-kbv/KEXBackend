import time
from copy import deepcopy
from typing import Optional, Type, Tuple, Dict, Union

from celery import Task
from requests import Session
from requests.models import Response
from requests.exceptions import HTTPError, ConnectionError, Timeout

from apps.pipeline import ServiceStatuses
from apps.common.models import ServiceHistoryModel
from apps.pipeline.exceptions import ServiceUnavailable


class BaseBackgroundService(Task):
    save_serializer: Optional[Type] = None
    autoretry_for: Tuple[Exception] = (Timeout, HTTPError, ConnectionError)  # noqa
    retry_kwargs: Dict = {"max_retries": 5}
    default_retry_delay: int = 1


class BaseService(Task):
    save_serializer: Optional[Type] = None

    autoretry_for: Tuple[Exception] = (Timeout, HTTPError, ConnectionError)  # noqa
    retry_kwargs: Dict = {"max_retries": 5}
    default_retry_delay: int = 1

    _session: Optional[Session] = None
    url: str
    method: str = 'POST'
    auth: Optional[Tuple[str, str]] = None
    cert: Optional[Tuple[str, str]] = None
    host_verify: bool = True
    timeout = 45

    history_url: str
    history_method: str = 'POST'
    status: ServiceStatuses
    data: Dict
    last_request: Union[bytes, str, None] = ''
    last_response: Union[bytes, str, None] = ''
    runtime: float = 0

    def __init__(self, instance, **kwargs):
        self.instance = instance
        self.kwargs = kwargs
        self.status = ServiceStatuses.NO_REQUEST

    @property
    def session(self) -> Session:
        if self._session is None:
            self._session = Session()

        self._session.hooks["response"].append(self.history)
        return self._session

    def history(self, response: Response, *args, **kwargs):
        self.last_request = response.request.body
        self.last_response = response.text

    def fetch(self, params=None, data=None, json=None, files=None, **kwargs):
        _start = time.perf_counter()

        self.last_request = ""

        response_raw = self.session.request(
            method=self.method,
            url=self.url,
            auth=self.auth,
            params=params,
            data=data,
            json=json,
            files=files,
            timeout=self.timeout,
            verify=self.host_verify,
            **kwargs
        )

        self.runtime = time.perf_counter() - _start

        if response_raw.status_code == 400:
            return self.handle_400(response_raw)

        if response_raw.status_code == 404:
            return self.handle_404(response_raw)

        return self.get_response(response_raw)

    def handle_400(self, response: Response): # noqa
        return response.json()

    def handle_404(self, response: Response): # noqa
        return response.text

    def handle_500(self, response: Response):
        raise ServiceUnavailable

    def get_response(self, response: Response): # noqa
        return response.json()

    def get_instance(self):
        return self.instance

    def run_service(self):
        # run_service should implement self.fetch method
        raise NotImplementedError

    def run(self):
        response_data = None

        try:
            response_data = self.run_service()
            self.data = deepcopy(response_data)
            self.save(response_data)

        except ServiceUnavailable:
            print(f"Service is unavailable {self.__class__.__name__}")
            self.status = ServiceStatuses.SERVICE_UNAVAILABLE

        except TimeoutError:
            raise TimeoutError

        except Exception as exc:
            print(f"Exception({self.__class__.__name__}): {exc.__class__} {exc}")
            self.status = ServiceStatuses.REQUEST_ERROR

        else:
            self.status = ServiceStatuses.WAS_REQUEST

        finally:
            self.log_save()
            self.kill_session()

        return response_data

    def log_save(self, instance=None):
        if not instance:
            instance = self.instance

        if hasattr(instance, 'history'):
            history_model: Type[ServiceHistoryModel] = instance.history.model
            history = history_model.objects.create(  # noqa
                content_object=instance,
                service=self.__class__.__name__,
                data=getattr(self, 'data', None),
                status=getattr(self, 'status', ServiceStatuses.NO_REQUEST),
                runtime=getattr(self, 'runtime', 0),
            )

            try:
                history.set_response(
                    url=self.url,
                    method=self.method,
                    request=self.last_request,
                    response=self.last_response,
                )
            except Exception as exc:
                print('Exception:', exc)
