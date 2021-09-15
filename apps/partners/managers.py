from django.db.models import QuerySet
from django.db.models.manager import BaseManager
from django.utils.timezone import localtime


class LocalBrandQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)


class LocalBrandManager(BaseManager.from_queryset(LocalBrandQuerySet)):
    """reserved"""
    ...


class BranchesQuerySet(QuerySet):
    def active(self):
        return self.filter(
            is_alive=True,
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
