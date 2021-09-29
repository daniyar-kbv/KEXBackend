from django.db.models import QuerySet, Q, F
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

        # returns a list of delivery_times that have start_time less than their end times
        list_1 = self.filter(
            Q(start_time__lte=F('end_time')), Q(start_time__lte=l_time), end_time__gte=l_time
        )

        # returns a list of delivery_times that have start_time greater than their end times
        list_2 = self.filter(
            Q(start_time__gt=F('end_time')), Q(start_time__lte=l_time) | Q(end_time__gte=l_time)
        )

        return list_1 | list_2


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
