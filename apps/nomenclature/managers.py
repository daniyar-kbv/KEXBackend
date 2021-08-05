from django.db.models import QuerySet
from django.db.models.manager import BaseManager


class BranchPositionQuerySet(QuerySet):
    def additional_positions(self):
        return self.filter(is_additional=True, position_type="MODIFIER")

    def main_positions(self):
        return self.filter(position_type="DISH")


class BranchPositionManager(BaseManager.from_queryset(BranchPositionQuerySet)):
    """reserved"""
    ...
