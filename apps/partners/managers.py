from django.db.models import QuerySet
from django.db.models.manager import BaseManager
from django.utils.timezone import localtime

from apps.partners import PlatformTypes, BrandImageTypes


class LocalBrandQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)


class LocalBrandManager(BaseManager.from_queryset(LocalBrandQuerySet)):
    """reserved"""
    ...


class BranchesQuerySet(QuerySet):
    def active(self):
        return self.filter(
            is_active=True,
            outer_id__isnull=False,
            terminal_id__isnull=False,
        )


class BranchDeliveryTimeQuerySet(QuerySet):
    def open(self):
        l_time = localtime().time()

        return self.filter(
            start_time__lte=l_time,
            end_time__gte=l_time,
        )


class BrandImageQuerySet(QuerySet):
    def for_web(self):
        return self.filter(size=PlatformTypes.WEB)

    def for_mobile(self):
        return self.filter(size=PlatformTypes.MOBILE)

    def image_longs(self):
        return self.filter(image_type=BrandImageTypes.IMAGE_LONG)

    def image_squares(self):
        return self.filter(image_type=BrandImageTypes.IMAGE_SQUARE)

    def image_shorts(self):
        return self.filter(image_type=BrandImageTypes.IMAGE_SHORT)

    def image_talls(self):
        return self.filter(image_type=BrandImageTypes.IMAGE_TALL)
