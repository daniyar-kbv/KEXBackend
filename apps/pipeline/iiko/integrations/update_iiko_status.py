from .base import BaseIIKOService

from apps.orders.models import Order
from apps.orders import OrderStatuses

from .serializers import IIKOOrderStatusSerializer


class UpdateOrderStatus(BaseIIKOService):
    """Обновление статуса заказа"""
    endpoint = 'api/1/deliveries/by_id'
    instance: Order = None
    save_serializer = IIKOOrderStatusSerializer

    _ORDER_STATUS_MAPPING = {
        'Unconfirmed': OrderStatuses.UNCONFIRMED,
        'ReadyForCooking': OrderStatuses.READY_FOR_COOKING,
        'CookingStarted': OrderStatuses.COOKING_STARTED,
        'CookingCompleted': OrderStatuses.COOKING_COMPLETED,
        'Waiting': OrderStatuses.WAITING,
        'OnWay': OrderStatuses.ON_WAY,
        'Delivered': OrderStatuses.DELIVERED,
        'Closed': OrderStatuses.DONE,
        'Cancelled': OrderStatuses.CANCELLED,
    }

    log_headers = True
    log_request = True
    log_response = True

    def get_local_brand_pk(self):
        return self.instance.local_brand_id  # noqa

    def map_order_status(self, iiko_status: str) -> str:
        return self._ORDER_STATUS_MAPPING.get(iiko_status)

    def run_service(self):
        return self.fetch(json={
            "organizationId": str(self.instance.branch.outer_id),
            "orderIds": [str(self.instance.outer_id)]
        })

    def prepare_to_save(self, data: dict):
        try:
            return {
                'status': self.map_order_status(data['orders'][0]['order']['status'])
            }
        except Exception as exc:
            ...

    def save(self, prepared_data):
        prepared_data = self.prepare_to_save(prepared_data)

        if not prepared_data:
            return

        serializer = self.save_serializer(
            instance=self.instance,
            data=prepared_data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
