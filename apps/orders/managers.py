from typing import TYPE_CHECKING

from django.db.models.manager import BaseManager

if TYPE_CHECKING:
    from .models import Lead


class OrdersManager(BaseManager):
    def create_from_lead(self, lead: 'Lead'):
        order = self.create(  # noqa
            lead=lead,
        )

        return order
