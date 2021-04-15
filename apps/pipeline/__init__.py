from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

default_app_config = 'apps.pipeline.apps.PipelineConfig'


class ServiceStatuses(TextChoices):
    NO_REQUEST = "NO_REQUEST", _('Не было запроса')
    WAS_REQUEST = "WAS_REQUEST", _('Был запрос')
    REQUEST_ERROR = "REQUEST_ERROR", _('Ошибка запроса')
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE", _('Сервис не доступен')