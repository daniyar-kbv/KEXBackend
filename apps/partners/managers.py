from django.db.models import QuerySet
from django.db.models.manager import BaseManager


class IIKOBrandQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)


class IIKOBrandManager(BaseManager.from_queryset(IIKOBrandQuerySet)):
    """reserved"""
    ...


class OrganizationsQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True)
