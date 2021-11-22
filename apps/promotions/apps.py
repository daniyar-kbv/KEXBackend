from django.apps import AppConfig


class PromotionsConfig(AppConfig):
    name = 'apps.promotions'

    def ready(self):
        from .beat_tasks import debut_contest_stats
