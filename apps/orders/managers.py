from typing import TYPE_CHECKING

from django.db.models.manager import BaseManager, Manager

if TYPE_CHECKING:
    from .models import Lead
    from apps.users.models import User


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
                "local_brand": lead.local_brand,
            },
        )

        return order

    def get_or_create_from_lead(self, user: 'User', lead: 'Lead'):
        order, created = self.get_or_create(
            lead=lead,
            defaults={
                "user": user,
                "cart": lead.cart
            }
        )

        user.addresses.get_or_create(
            address=lead.address,
            defaults={
                "local_brand": lead.local_brand,
            }
        )

        return order
