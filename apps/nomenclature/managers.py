from django.db.models import QuerySet
from django.db.models.manager import BaseManager, Manager


class BranchPositionQuerySet(QuerySet):
    def active(self):
        return self.filter(is_exists=True, is_active=True, position__is_active=True)

    #def additional_positions(self):
    #    return self.active().filter(position__is_additional=True, position__position_type="MODIFIER")

    def main_positions(self):
        return self.active() #.filter(position__position_type="DISH")


class BranchPositionManager(BaseManager.from_queryset(BranchPositionQuerySet)):
    def get_queryset(self):
        return super(BranchPositionManager, self).get_queryset().select_related('position')

#
# class BranchCategoryQuerySet(QuerySet):
#     def active(self):
#         return self.filter(
#             is_active=True, category__is_active=True, branch_positions__isnull=False,
#         ).distinct()

#
# class BranchCategoryManager(BaseManager.from_queryset(BranchCategoryQuerySet)):
#     def get_queryset(self):
#         return super(BranchCategoryManager, self).get_queryset()\
#             .select_related('category')\
#             .prefetch_related('branch_positions')
#

class PositionModifierGroupManager(Manager):
    def get_queryset(self):
        return super(PositionModifierGroupManager, self).get_queryset().select_related('modifier_group')
