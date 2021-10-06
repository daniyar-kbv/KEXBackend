default_app_config = 'apps.promotions.apps.PromotionsConfig'

from django.db.models import TextChoices


class PromotionTypes(TextChoices):
    ARTICLE = ('ARTICLE', 'Статья')
    CONTEST = ('CONTEST', 'Конкурс')
    CONTEST_DEBUT = ('CONTEST_DEBUT', 'Конкурс на открытие сервиса')
