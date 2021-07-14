from decimal import Decimal
from .integrations.payment import PaymentService

from apps.payments.models import Payment


def _make_payment(payment: Payment):
    c = '014111111111231202PAYp0rKLqsXz+XSzKBe56Q16MpuRNQvXjNwpPRU1N0Sxmlm7PQcX0tt70Gn+rLDlWsZGOzYSZqkgkZeOmoDJR8je/ej5wE2WuzlGjJ601GSsul9b7w4rkNON4iWx9RCU+pRRvRGiHEnWiU+gGHg00769YHmdQ3LPvPdORH/dlHEFJ9pO370yqArizmCEQeI2aCqvYpjgBxF2u8xeRTvPsxXg+C2by3p7iCxqiukC8golQ8cRnz67YfzWgP6jYABbDW9C7gqPpgBiWWLjYvRLX8eKKnccoUOkaT93DR7+QwZ4LYmnvOsDTqnyNHIxxlehY3iHUhww7XAFcfcT756N/g=='


def make_payment(payment_pk: int):
    payment = Payment.objects.select_related('debit_card').get(pk=payment_pk)


    res = PaymentService(instance=payment).run()
    print(res)
    return res