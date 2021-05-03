from django.apps import AppConfig


class PipelineConfig(AppConfig):
    name = 'apps.pipeline'

    def ready(self):
        super().ready()
        from .iiko import celery_tasks
