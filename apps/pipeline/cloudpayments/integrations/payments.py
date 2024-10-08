from typing import TYPE_CHECKING, Dict

from apps.payments import PaymentStatusTypes

from .base import BaseCloudPaymentsService
from .serializers import CloudPaymentsPaymentSerializer

if TYPE_CHECKING:
    from apps.payments.models import Payment


class PaymentBaseService(BaseCloudPaymentsService):
    save_serializer = CloudPaymentsPaymentSerializer
    instance: 'Payment'

    log_response = True
    log_request = True
    log_headers = True
    _status_mapping = {
        "Completed": PaymentStatusTypes.COMPLETED,
        "Cancelled": PaymentStatusTypes.CANCELLED,
        "Declined": PaymentStatusTypes.DECLINED,
    }

    def get_status(self, data: Dict) -> str:
        cloud_payments_status = data.get("Status")
        if all([
            not cloud_payments_status,
            data.get("AcsUrl"),
            data.get("PaReq")
        ]):
            return PaymentStatusTypes.AWAITING_AUTHENTICATION

        return self._status_mapping.get(cloud_payments_status, PaymentStatusTypes.DECLINED)

    def prepare_to_save(self, data: Dict) -> Dict:
        model = data.get("Model", {})

        return {
            "status": self.get_status(model),
            "reason_code": model.get("ReasonCode"),
            "rrn": model.get("Rrn", self.instance.rrn),
            "pa_req": model.get("PaReq", self.instance.pa_req),
            "acs_url": model.get("AcsUrl", self.instance.acs_url),
            "outer_id": model.get("TransactionId", self.instance.outer_id),
            "debit_card": {
                "card_token": model.get("Token"),
                "card_type": model.get("CardType"),
                "card_holder_name": model.get("Name"),
                "card_account_id": model.get("AccountId"),
                "card_expiration_date": model.get("CardExpDate"),
                "card_masked_number": model.get("CardLastFour"),
            },
        }

    def finalize_response(self, response):
        # print(response)
        return super().finalize_response(response)


class PaymentService(PaymentBaseService):
    """Проведение платежа"""
    endpoint = "/payments/cards/charge"

    def run_service(self):
        return self.fetch(json={
            'Amount': str(self.instance.price),
            'Currency': self.instance.currency,
            'AccountId': str(self.instance.user.secret_key),
            'IpAddress': self.instance.ip_address,
            'Name': self.instance.card_holder_name,
            'CardCryptogramPacket': self.instance.cryptogram
        })


class CardPaymentService(PaymentBaseService):
    """Проведение платежа сохраненной картой"""

    endpoint = "/payments/tokens/charge"

    def run_service(self):
        return self.fetch(json={
            'Amount': str(self.instance.price),
            'Currency': self.instance.currency,
            'IpAddress': self.instance.ip_address,
            'AccountId': self.instance.debit_card.card_account_id,
            'Token': self.instance.debit_card.card_token,
        })


class Confirm3DSService(PaymentBaseService):
    """Подтверждение платежа"""

    endpoint = "/payments/cards/post3ds"

    def run_service(self):
        return self.fetch(json={
            'TransactionId': self.instance.outer_id,
            'PaRes': self.instance.pa_res,
        })
