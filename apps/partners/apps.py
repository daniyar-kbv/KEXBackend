from django.apps import AppConfig


class PartnersConfig(AppConfig):
    name = 'apps.partners'

    def ready(self):
        from . import signals
