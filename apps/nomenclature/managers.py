from django.db.models import QuerySet
from django.db.models.manager import BaseManager


class BranchPositionQuerySet(QuerySet):
    def additional_positions(self):
        return self.filter(is_additional=True)

    def main_positions(self):
        return self.filter(is_additional=False)


class BranchPositionManager(BaseManager.from_queryset(BranchPositionQuerySet)):
    """reserved"""
    ...
