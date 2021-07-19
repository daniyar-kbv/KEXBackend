from typing import TYPE_CHECKING

from django.db.models.manager import BaseManager, Manager

if TYPE_CHECKING:
    from .models import Lead


class OrdersManager(Manager):
    def create_from_lead(self, user, lead: 'Lead'):
        order = self.create(  # noqa
            lead=lead,
            user=user,
            cart=lead.cart,
        )
        user.addresses.get_or_create(
            address=lead.address,
            defaults={
                "is_current": True,
                "local_brand": lead.local_brand,
            },
        )

        return order
