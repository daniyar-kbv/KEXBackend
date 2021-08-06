from django.db.models import QuerySet
from django.db.models.manager import BaseManager


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
