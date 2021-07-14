from typing import TYPE_CHECKING, Dict

from apps.payments import PaymentStatusTypes

from .base import BaseCloudPaymentsService
from .entities import PaymentResponse
from .serializers import CloudPaymentsPaymentSerializer
if TYPE_CHECKING:
    from apps.payments.models import Payment

from cloudpayments import CloudPayments


class PaymentService(BaseCloudPaymentsService):
    endpoint = "/payments/cards/charge"
    instance: 'Payment'
    save_serializer = CloudPaymentsPaymentSerializer

    _status_mapping = {
        "Completed": PaymentStatusTypes.COMPLETED,
        "Cancelled": PaymentStatusTypes.CANCELLED,
        "Declined": PaymentStatusTypes.DECLINED,
    }

    def run_service(self):
        return self.fetch({
            'Amount': self.instance.price,
            'Currency': self.instance.currency,
            'IpAddress': self.instance.ip_address,
            'Name': self.instance.debit_card.card_holder_name,
            'CardCryptogramPacket': self.instance.cryptogram
        })

    def get_status(self, cloud_payments_status: str) -> str:
        return self._status_mapping.get(cloud_payments_status)

    def get_card_masked_number(self, card_last_four: str) -> str:
        return f"**** **** **** {card_last_four}"

    def prepare_to_save(self, data: Dict) -> Dict:
        model = data.get("Model", {})
        res = PaymentResponse(
            success=data.get("Success"),
            rrn=model.get("Rrn"),
            outer_id=model.get("TransactionId"),
            reason_code=model.get("ReasonCode"),
            status=self.get_status(model.get("Status")),
            card_type=model.get("CardType"),
            card_expiration_date=model.get("CardExpDate"),
            card_masked_number=self.get_card_masked_number(model.get("CardLastFour")),
        ).__dict__

        # print(res)
        return res
