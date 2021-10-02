from typing import TYPE_CHECKING, Iterable, cast

from .base import BaseIIKOService

from apps.orders.models import Order
from apps.orders import OrderStatuses

from .serializers import IIKOOrderIDSerializer

if TYPE_CHECKING:
    from apps.payments.models import Payment


CREATION_STATUS_MAPPING = {
    "InProgress": OrderStatuses.APPLYING,
    "Success": OrderStatuses.APPLIED,
}


class ApplyDeliveryOrder(BaseIIKOService):
    """Создание заказа в системе IIKO"""
    endpoint = 'api/1/deliveries/create'
    save_serializer = IIKOOrderIDSerializer
    instance: 'Order' = None

    log_headers = True
    log_request = True
    log_response = True

    def __init__(self, instance=None, **kwargs):
        self.payment: 'Payment' = instance.completed_payment
        super().__init__(instance, **kwargs)

    def skip_task(self):
        if self.instance.status in [OrderStatuses.APPLYING, OrderStatuses.APPLIED]:
            return True

    def get_local_brand_pk(self):  # noqa
        return self.instance.local_brand_id

    def run_service(self):
        return self.fetch(json={
            'organizationId': str(self.instance.branch.outer_id),
            'terminalGroupId': str(self.instance.branch.terminal_id),
            'createOrderSettings': {
                'transportToFrontTimeout': 20
            },
            'order': {
                'comment': str(self.instance.lead.address.full_address()),
                'phone': str(self.instance.user.mobile_phone),
                'customer': {'name': self.instance.user.name},
                'orderServiceType': 'DeliveryByCourier',
                'deliveryPoint': {
                    'coordinates': {
                        'latitude': str(self.instance.lead.address.latitude),
                        'longitude': str(self.instance.lead.address.longitude)
                    },
                },
                'payments': [
                    {
                        'sum': float(self.payment.price),
                        'isProcessedExternally': False,
                        'paymentTypeId': str(self.instance.local_brand.current_payment_type_id),
                        'paymentTypeKind': self.instance.local_brand.current_payment_type_code,
                    }
                ],
                'items': [{
                        'type': 'Product',
                        'productId': str(position.branch_position.outer_id),
                        'amount': position.count,
                        'comment': position.comment or "no_comment",
                        'modifiers': [{
                            'productId': str(modifier.branch_position.outer_id),
                            'productGroupId': str(modifier.position_modifier_group.modifier_group.outer_id),
                            'amount': modifier.count,
                        } for modifier in cast(Iterable['CartPositionModifier'], position.modifiers.all())] or None
                } for position in cast(Iterable['CartPosition'], self.instance.cart.positions.all())]
            }
        })

    def prepare_to_save(self, data: dict) -> dict:
        prepared_data = {}
        order_info = data.get('orderInfo', {})
        outer_id = order_info.get('id')

        if outer_id:
            status = CREATION_STATUS_MAPPING.get(order_info.get('creationStatus'))
            prepared_data['outer_id'] = outer_id
            prepared_data['status'] = status

        return prepared_data

    def save(self, prepared_data):
        serializer = self.save_serializer(
            instance=self.instance,
            data=self.prepare_to_save(prepared_data),
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
