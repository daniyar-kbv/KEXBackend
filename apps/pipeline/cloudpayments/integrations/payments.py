from typing import TYPE_CHECKING, Dict

from apps.payments import PaymentStatusTypes

from . import entities
from .base import BaseCloudPaymentsService
from .serializers import CloudPaymentsPaymentSerializer

if TYPE_CHECKING:
    from apps.payments.models import Payment


class PaymentBaseService(BaseCloudPaymentsService):
    save_serializer = CloudPaymentsPaymentSerializer

    def get_status(self, data: Dict) -> str:
        cloud_payments_status = data.get("Status")
        if all([
            not cloud_payments_status,
            data.get("AcsUrl"),
            data.get("PaReq")
        ]):
            return PaymentStatusTypes.AWAITING_AUTHENTICATION

        return self._status_mapping.get(cloud_payments_status, PaymentStatusTypes.DECLINED)

    def get_card_masked_number(self, card_last_four: str) -> str:
        if card_last_four is not None:
            return f"**** **** **** {card_last_four}"

    def prepare_to_save(self, data: Dict) -> Dict:
        # data = {
        #     "Model": {
        #         "TransactionId": 504,
        #         "PaReq": "eJxVUdtugkAQ/RXDe9mLgo0Z1nhpU9PQasWmPhLYAKksuEChfn13uVR9mGTO7MzZM2dg3qSn0Q+X\nRZIJxyAmNkZcBFmYiMgxDt7zw6MxZ+DFkvP1ngeV5AxcXhR+xEdJ6BhpEZnEYLBdfPAzg56JKSKT\nAhqgGpFB7IuSgR+cl5s3NqFTG2NAPYSUy82aETqeWPYUUAdB+ClnwSmrwtz/TbkoC0BtDYKsEqX8\nZfZkDGgAUMkTi8synyFU17V5N2nKCpBuAHRVs610VijCJgmZu17UXTxhFWP34l7evYPlegsHkO6A\n0C85o5hMsI3piNIZHc+IBaitg59qJYzgdrUOQK7/WNy+3FZAeSqV5cMqAwLe5JlQwpny8T8HdFW8\netFuBqUyahV+Hjf27vWCaSx22fe+KY6kXKZfJLK1x22TZkyUS8QiHaUGgDQN6s+H+tOq7O7kf8hd\nt30=",
        #         "AcsUrl": "https://test.paymentgate.ru/acs/auth/start.do"
        #     },
        #     "Success": False,
        #     "Message": None
        # }
        model = data.get("Model", {})
        payment_response = entities.PaymentResponse(
            payment_transaction=entities.PaymentTransaction(
                rrn=model.get("Rrn"),
                outer_id=model.get("TransactionId"),
                reason_code=model.get("ReasonCode"),
                status=self.get_status(model),
            ),
            debit_card=entities.DebitCard(
                card_token=model.get("Token"),
                card_type=model.get("CardType"),
                card_expiration_date=model.get("CardExpDate"),
                card_masked_number=self.get_card_masked_number(model.get("CardLastFour")),
            ),
            authorization_3ds=entities.Authorization3DS(
                acs_url=model.get("AcsUrl"),
                pa_req=model.get("PaReq"),
            ),
        )

        return {
            **payment_response.payment_transaction.__dict__,
            **payment_response.debit_card.__dict__,
            **payment_response.authorization_3ds.__dict__,
        }


class PaymentService(PaymentBaseService):
    endpoint = "/payments/cards/charge"
    instance: 'Payment'

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


class Confirm3DSService(PaymentBaseService):
    endpoint = "/payments/cards/post3ds"
    instance: 'Payment'
    save_serializer = None

    def run_service(self):
        return self.fetch({
            'TransactionId': self.instance.outer_id,
            'PaRes': self.instance.pa_res,
        })
