from typing import TYPE_CHECKING, Iterable, cast

from .base import BaseIIKOService

from apps.orders.models import Order
from apps.orders import OrderStatuses
from apps.payments import PaymentTypes
from apps.partners import RequiredLocalBrandPaymentTypes

from .serializers import IIKOOrderIDSerializer

if TYPE_CHECKING:
    from apps.payments.models import Payment
    from apps.partners.models import LocalBrandPaymentType


class BaseApplyOrder(BaseIIKOService):
    save_serializer = IIKOOrderIDSerializer
    instance: 'Order' = None

    _CREATION_STATUS_MAPPING = {
        "InProgress": OrderStatuses.APPLYING,
        "Success": OrderStatuses.APPLIED,
    }

    def skip_task(self):
        if self.instance.status == OrderStatuses.APPLIED:
            return True

    def get_local_brand_pk(self):
        return self.instance.local_brand_id  # noqa

    def map_creation_status(self, iiko_status: str) -> str:
        return self._CREATION_STATUS_MAPPING.get(iiko_status)

    def save(self, prepared_data):
        serializer = self.save_serializer(
            instance=self.instance,
            data=self.prepare_to_save(prepared_data),
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()


class ApplyDeliveryOrder(BaseApplyOrder):
    """Создание заказа в системе IIKO"""
    endpoint = 'api/1/deliveries/create'
    log_request = True
    log_response = True
    log_headers = True

    def __init__(self, instance=None, **kwargs):
        print('self.instance ApplyDeliveryOrder', instance)
        self.instance = instance
        self.payment: 'Payment' = instance.completed_payment
        self.iiko_payment_type: 'LocalBrandPaymentType' = self.get_iiko_payment_type(self.payment.payment_type)

        super().__init__(instance, **kwargs)

    def get_iiko_payment_type(self, completed_payment_type):
        payment_mapping = {
            PaymentTypes.CASH: RequiredLocalBrandPaymentTypes.CASH
        }

        return self.instance.lead.local_brand.payment_types.filter(
            payment_type=payment_mapping.get(completed_payment_type, RequiredLocalBrandPaymentTypes.CARD)
        ).first()

    def get_comment(self):
        if self.payment.payment_type == PaymentTypes.CASH \
                and self.payment.price != self.instance.cart.total_price:
            return f"Нужна сдача с {self.payment.price}"

        return ""

    def run_service(self):
        return self.fetch(json={
            'organizationId': str(self.instance.branch.outer_id),
            'terminalGroupId': str(self.instance.branch.terminal_id),
            'createOrderSettings': {
                'transportToFrontTimeout': 20
            },
            'order': {
                'comment': self.get_comment(),
                'phone': str(self.instance.user.mobile_phone),
                'customer': {'name': self.instance.user.name},
                'orderServiceType': 'DeliveryByCourier',
                'deliveryPoint': {
                    'coordinates': {
                        'latitude': str(self.instance.lead.address.latitude),
                        'longitude': str(self.instance.lead.address.longitude)
                    },
                    'comment': str(self.instance.lead.address.full_address()),
                },
                'payments': [
                    {
                        'sum': float(self.payment.price),
                        'isProcessedExternally': False,
                        'paymentTypeId': str(self.iiko_payment_type.uuid) if self.iiko_payment_type else None,
                        'paymentTypeKind': self.iiko_payment_type.code if self.iiko_payment_type else None,
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
            status = self.map_creation_status(order_info.get('creationStatus'))
            prepared_data['outer_id'] = outer_id
            if status:
                prepared_data['status'] = status

        return prepared_data


class VerifyDeliveryOrder(BaseApplyOrder):
    """Валидация просадки заказа в сервис IIKO"""
    endpoint = 'api/1/deliveries/by_id'

    def skip_task(self):
        if self.instance.outer_id is None:
            return True

        return super().skip_task()

    def run_service(self):
        return self.fetch(json={
            "organizationId": str(self.instance.branch.outer_id),
            "orderIds": [str(self.instance.outer_id)]
        })

    def prepare_to_save(self, data: dict) -> dict:
        prepared_data = {}
        orders = data.get('orders', [])
        if not orders or not isinstance(orders, list):
            return prepared_data

        order_info = orders[0]
        outer_id = order_info.get('id')

        if outer_id:
            status = self.map_creation_status(order_info.get('creationStatus'))
            prepared_data['outer_id'] = outer_id
            if status:
                prepared_data['status'] = status

        return prepared_data
