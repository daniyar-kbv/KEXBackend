from requests import Session
from typing import Optional, Union, Type, ClassVar

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.module_loading import import_string

from zeep import Client


class SmsBackendInterface:
    def send_sms(
            self,
            sender: str,
            recipient: str,
            message: str,
            client_message_id: Optional[Union[int, str]] = None,
            **kwargs
    ):
        raise NotImplementedError()

    def send_sms_batch(
            self,
            *args,
            **kwargs
    ):
        raise NotImplementedError()

    def message_info(self, *args, **kwargs):
        raise NotImplementedError()

    def bulk_message_info(self, *args, **kwargs):
        raise NotImplementedError()


class BaseSmsBackend:
    url: ClassVar[Union[str, None]] = None

    def __init__(
            self,
            username: str,
            password: str,
            message_id:
            Optional[Union[str, int]] = None
    ) -> None:
        self.username = username
        self.password = password
        self.message_id = message_id
        self.client = self._init_client()

    def _init_client(self) -> Union[Client, Session]:
        raise NotImplementedError()


class KazInfoTeh(BaseSmsBackend, SmsBackendInterface):
    url = 'http://isms.center/soap'

    def _init_client(self):
        return Client(self.url)

    def _run_service(self, service, **kwargs):
        kwargs.update({
            'login': self.username,
            'password': self.password
        })
        return self.client.service[service](**kwargs)

    def send_sms(
            self,
            sender: str,
            recipient: str,
            message: str,
            client_message_id: Optional[Union[int, str]] = None,
            msg_type: Optional[int] = 0,
            scheduled: Optional[str] = '',
            priority: Optional[int] = 1
    ):
        sms_type = self.client.get_type('ns0:SMSM')
        params = {
            'recepient': recipient,
            'senderid': sender,
            'msg': message,
            'msgtype': msg_type,
            'scheduled': scheduled,
            'UserMsgID': client_message_id,
            'prioritet': priority
        }
        result = self._run_service('SendMessage', **{'sms': sms_type(**params)})
        if result.MsgID is not None:
            self.message_id = result.MsgID
        return result

    def send_sms_batch(self, *args, **kwargs):
        pass

    def message_info(self, client_message_id: Optional[Union[str, int]] = None):
        key = 'MsgID'
        message_id = client_message_id or self.message_id
        if client_message_id:
            key = 'UserMsgID'
        sms_type = self.client.get_type('ns0:IDSMS')
        return self._run_service('SendMessage', **{'sms': sms_type(**{key: message_id})})

    def bulk_message_info(self, *args, **kwargs):
        pass


class SmsConsult(BaseSmsBackend, SmsBackendInterface):
    url = 'http://service.sms-consult.kz'
    outbound_template = 'sms/outbound.xml'
    info_template = 'sms/info.xml'

    def bulk_message_info(self, *args, **kwargs):
        pass

    def send_sms_batch(self, *args, **kwargs):
        pass

    def message_info(self, client_message_id: Optional[Union[str, int]] = None):
        data = {
            'messages_info': [{'id': client_message_id}],
            'login': self.username,
            'password': self.password
        }
        return self.client.post(self.url, data=self.post_data(data, self.info_template))

    @staticmethod
    def post_data(data, template_name):
        return render_to_string(
            template_name,
            context=data
        ).encode('utf-8')

    def _init_client(self):
        session = Session()
        session.headers = {'content_type': 'application/xml'}
        return session

    def send_sms(
            self,
            sender: str,
            recipient: str,
            message: str,
            client_message_id: Optional[Union[int, str]] = None,
            msg_type: Optional[int] = 0,
            scheduled: Optional[str] = '',
            priority: Optional[int] = 1
    ):
        data = {
            'login': self.username,
            'password': self.password,
            'messages': [{
                'sender': sender,
                'recipient': recipient,
                'id': client_message_id,
                'message': message
            }]
        }
        return self.client.post(self.url, data=self.post_data(data, template_name=self.outbound_template))


def sms_backend(*args, **kwargs) -> SmsBackendInterface:
    return import_string(
        settings.SMS_BACKEND
    )(*args, **kwargs)
