"""
CloudPayments Hooks
https://developers.cloudpayments.ru/#check
# todo validate host domain, only for cloudpayments.kz
"""

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.common.mixins import PublicAPIMixin

from . import PaymentStatusTypes
from .models import Payment

SUCCESS_CODE = 0
FAILURE_CODE = 13


def generate_failure_code():
    return {'code': FAILURE_CODE}


def generate_success_code():
    return {'code': SUCCESS_CODE}


def get_payment(invoice_id: str = None):
    if not invoice_id or not Payment.objects.in_progress().filter(uuid=invoice_id).exists():
        return

    return Payment.objects.select_related('order').get(uuid=invoice_id)


class CloudPaymentsCheckView(PublicAPIMixin, APIView):
    def post(self, request, *args, **kwargs):
        print(f"{self.__class__.__name__} (request):", request.data)
        if not request.data.get('InvoiceId'):
            return Response(data=generate_success_code())

        payment = get_payment(invoice_id=request.data.get('InvoiceId'))

        if not payment or payment.order.is_completed_payment_exists:
            return Response(data=generate_failure_code())

        return Response(data=generate_success_code())


class SuccessView(PublicAPIMixin, APIView):
    def post(self, request, *args, **kwargs):
        print("SUCCESS_VIEW (request):", request.data)
        if not request.data.get('InvoiceId'):
            return Response(data=generate_success_code())

        payment = get_payment(invoice_id=request.data.get('InvoiceId'))

        if not payment:
            return Response(data=generate_failure_code())

        payment.change_status(PaymentStatusTypes.COMPLETED)

        return Response(data=generate_success_code())


class FailureView(PublicAPIMixin, APIView):
    def post(self, request, *args, **kwargs):
        print("FAILURE_VIEW (request):", request.data)
        if not request.data.get('InvoiceId'):
            return Response(data=generate_success_code())

        payment = get_payment(invoice_id=request.data.get('InvoiceId'))

        if not payment:
            return Response(data=generate_failure_code())

        payment.change_status(PaymentStatusTypes.DECLINED)

        return Response(data=generate_success_code())
