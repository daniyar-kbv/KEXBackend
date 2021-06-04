from django.apps import AppConfig


class NomenclatureConfig(AppConfig):
    name = 'apps.nomenclature'

    def ready(self):
        from . import signals
