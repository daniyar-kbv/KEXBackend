from typing import TYPE_CHECKING

from .base import BaseIIKOService

if TYPE_CHECKING:
    from apps.orders.models import Order


class CancelDeliveryOrder(BaseIIKOService):
    """Отмена заказа в системе IIKO"""
    endpoint = 'api/1/deliveries/cancel'
    log_request = True
    log_response = True
    log_headers = True
    instance: 'Order' = None

    def skip_task(self):
        if not self.instance.outer_id:
            self.instance.mark_as_canceled()
            return True

        if not self.instance.is_allowed_to_cancel:
            return False

    def get_local_brand_pk(self):
        return self.instance.local_brand_id  # noqa

    def run_service(self):
        return self.fetch(json={
            'organizationId': str(self.instance.branch.outer_id),
            'orderId': str(self.instance.outer_id),
            'cancelCauseId': str(self.instance.local_brand.get_default_cancel_cause_uuid)
        })

    def finalize_response(self, response):
        if self.status_code == 200:
            self.instance.mark_as_canceled()
            return True

        return False
