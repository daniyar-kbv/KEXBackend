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

        return order
