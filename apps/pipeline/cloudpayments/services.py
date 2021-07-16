from .integrations.payments import PaymentService, Confirm3DSService

from apps.payments.models import Payment


def make_payment(payment_pk: int):
    payment = Payment.objects.select_related('debit_card').get(pk=payment_pk)
    return PaymentService(instance=payment).run()


def confirm_payment_3ds(payment_pk: int):
    payment = Payment.objects.select_related('debit_card').get(pk=payment_pk)
    return Confirm3DSService(instance=payment).run()
