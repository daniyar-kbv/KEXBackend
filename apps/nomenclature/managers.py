from django.db.models import QuerySet
from django.db.models.manager import BaseManager


class BranchPositionQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True, )

    def additional_positions(self):
        return self.active().filter(position__is_additional=True, position__position_type="MODIFIER")

    def main_positions(self):
        return self.active().filter(position__position_type="DISH")


class BranchPositionManager(BaseManager.from_queryset(BranchPositionQuerySet)):
    def get_queryset(self):
        return super(BranchPositionManager, self).get_queryset().select_related('position')


class BranchCategoryQuerySet(QuerySet):
    def active(self):
        return self.filter(is_active=True, category__is_active=True)


class BranchCategoryManager(BaseManager.from_queryset(BranchCategoryQuerySet)):
    def get_queryset(self):
        return super(BranchCategoryManager, self).get_queryset().select_related('category')
