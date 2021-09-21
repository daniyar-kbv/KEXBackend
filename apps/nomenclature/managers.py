from django.db.models import QuerySet
from django.db.models.manager import BaseManager, Manager


class BranchPositionQuerySet(QuerySet):
    def active(self):
        return self.filter(is_exists=True, is_active=True, position__is_active=True).distinct()

    def main_positions(self):
        return self.active()\
            .filter(position__position_type='MAIN')\
            .distinct()

    def additional_positions(self):
        return self.active()\
            .filter(position__position_type='ADDITIONAL')\


class BranchPositionManager(BaseManager.from_queryset(BranchPositionQuerySet)):
    def get_queryset(self):
        return super(BranchPositionManager, self).get_queryset().select_related('position')


class CategoryQuerySet(QuerySet):
    def active(self):
        return self.filter(
            is_active=True, branch_positions__isnull=False,
        ).distinct()


class CategoryManager(BaseManager.from_queryset(CategoryQuerySet)):
    ...


class PositionModifierGroupManager(Manager):
    def get_queryset(self):
        return super(PositionModifierGroupManager, self).get_queryset().select_related('modifier_group')
