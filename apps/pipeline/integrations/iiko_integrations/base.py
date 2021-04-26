from constance import config

from apps.pipeline.services import BaseService


class BaseIIKOService(BaseService):  # noqa
    host = config.IIKO_SERVICE_HOST
