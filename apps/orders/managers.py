from typing import TYPE_CHECKING

from django.db.models.manager import Manager, QuerySet

from apps.nomenclature.models.positions import PositionTypes

if TYPE_CHECKING:
    from .models import Lead


class CartPositionQueryset(QuerySet):
    def exclude_delivery(self):
        return self.exclude(
            branch_position__position__position_type__in=[
                PositionTypes.DAY_DELIVERY,
                PositionTypes.NIGHT_DELIVERY,
            ]
        )

    def only_delivery(self):
        return self.filter(
            branch_position__position__position_type__in=[
                PositionTypes.DAY_DELIVERY,
                PositionTypes.NIGHT_DELIVERY,
            ]
        )


class OrdersManager(Manager):
    def get_or_create_from_lead(self, lead: 'Lead'):
        order, created = self.get_or_create(
            lead=lead,
            defaults={
                "user": lead.user,
                "cart": lead.cart,
                "local_brand": lead.local_brand,
                "branch": lead.branch,
            }
        )

        # user.addresses.get_or_create(
        #     address=lead.address,
        #     defaults={
        #         "local_brand": lead.local_brand,
        #     }
        # )

        return order
