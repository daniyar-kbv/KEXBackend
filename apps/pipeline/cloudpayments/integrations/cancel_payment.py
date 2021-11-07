from typing import TYPE_CHECKING

from .base import BaseCloudPaymentsService

if TYPE_CHECKING:
    from apps.payments.models import Payment


class CancelPayment(BaseCloudPaymentsService):
    """Проведение отмены транзакции"""
    endpoint = 'payments/refund'
    instance: 'Payment'

    log_response = True
    log_request = True
    log_headers = True

    def run_service(self):
        return self.fetch(json={
            'Amount': str(self.instance.price),
            'TransactionId': str(self.instance.outer_id),
        })

    def finalize_response(self, response):
        print('FINALIZE_RESPONSE', response)
        success = response.get('Success')

        if success:
            self.instance.mark_as_cancelled()
            return True

        else:
            self.instance.cancel_error(response.get('Message'))
            return False
