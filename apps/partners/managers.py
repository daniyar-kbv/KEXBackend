from django.db.models import QuerySet, Q, F
from django.db.models.manager import BaseManager
from django.utils.timezone import localtime

from apps.common import PlatformTypes, ImageTypes

from . import RequiredLocalBrandPaymentTypes


class LocalBrandQuerySet(QuerySet):
    def active(self):
        return self.filter(
            is_active=True,
            cancel_causes__is_default=True,
            payment_types__payment_type__in=[
                RequiredLocalBrandPaymentTypes.CASH,
                RequiredLocalBrandPaymentTypes.CARD,
            ]
        ).distinct()


class LocalBrandManager(BaseManager.from_queryset(LocalBrandQuerySet)):
    ...


class BranchQuerySet(QuerySet):
    def active(self):
        return self.filter(
            is_active=True,
            local_brand__is_active=True,
            outer_id__isnull=False,
            terminal_id__isnull=False,
        )


class BranchManager(BaseManager.from_queryset(BranchQuerySet)):
    ...


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
