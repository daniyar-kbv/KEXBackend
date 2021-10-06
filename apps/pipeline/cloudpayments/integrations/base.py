from constance import config

from apps.pipeline.services import BaseService


class BaseCloudPaymentsService(BaseService):  # noqa
    host = config.CLOUDPAYMENTS_HOST
    auth = (
        config.CLOUDPAYMENTS_PUBLIC_KEY,
        config.CLOUDPAYMENTS_SECRET_KEY,
    )
