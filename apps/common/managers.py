from django.db.models import QuerySet
from django.db import models
import inspect
import sys

from . import PlatformTypes, ImageTypes


class MainManager(models.Manager):

    def get_queryset(self):
        queryset = super(MainManager, self).get_queryset()

        ml_classes = [c[1] for c in inspect.getmembers(sys.modules['apps.translations.models'], inspect.isclass)]
        rel_fields = []

        for f in queryset.model._meta.get_fields():
            if f.is_relation and hasattr(f, 'to_fields') and 'id' in f.to_fields:
                if f.related_model in ml_classes:
                    rel_fields.append(f.name)

        queryset = queryset.select_related(*rel_fields)
        return queryset


class ImageQuerySet(QuerySet):
    def for_web(self):
        return self.filter(platform=PlatformTypes.WEB)

    def for_mobile(self):
        return self.filter(platform=PlatformTypes.MOBILE)

    def image_longs(self):
        return self.filter(image_type=ImageTypes.IMAGE_LONG)

    def image_squares(self):
        return self.filter(image_type=ImageTypes.IMAGE_SQUARE)

    def image_shorts(self):
        return self.filter(image_type=ImageTypes.IMAGE_SHORT)

    def image_talls(self):
        return self.filter(image_type=ImageTypes.IMAGE_TALL)
