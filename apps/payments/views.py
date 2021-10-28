from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.db.models import Value, When, Case, BooleanField
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView

from apps.common.mixins import PublicAPIMixin, JSONRendererMixin

from . import PaymentStatusTypes
from .models import Payment, DebitCard
from .serializers import (
    DebitCardsSerializer,
    CreatePaymentSerializer,
    CreateCardPaymentSerializer,
    Confirm3DSPaymentSerializer,
    CreateWidgetPaymentSerializer,
)

from apps.orders.decorators import (
    check_branch_is_open_and_active,
    update_delivery_positions,
    check_out_of_stock,
)


@method_decorator(check_branch_is_open_and_active, name="post")
@method_decorator(check_out_of_stock, name='post')
@method_decorator(update_delivery_positions, name='post')
class CreatePaymentView(JSONRendererMixin, CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = CreatePaymentSerializer


@method_decorator(check_branch_is_open_and_active, name="post")
@method_decorator(check_out_of_stock, name='post')
@method_decorator(update_delivery_positions, name='post')
class CreateCardPaymentView(JSONRendererMixin, CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = CreateCardPaymentSerializer


@method_decorator(check_branch_is_open_and_active, name="post")
@method_decorator(check_out_of_stock, name='post')
@method_decorator(update_delivery_positions, name='post')
class CreateWidgetPaymentView(JSONRendererMixin, CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = CreateWidgetPaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.change_status(PaymentStatusTypes.IN_PROGRESS)


class Confirm3DSPaymentView(JSONRendererMixin, UpdateAPIView):
    allowed_methods = ["PUT"]
    queryset = Payment.objects.all()
    serializer_class = Confirm3DSPaymentSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "payment_uuid"


@method_decorator(check_branch_is_open_and_active, name="post")
@method_decorator(check_out_of_stock, name='post')
@method_decorator(update_delivery_positions, name='post')
class DebitCardsListViewSet(
    JSONRendererMixin,
    ModelViewSet,
):
    lookup_field = "uuid"
    queryset = DebitCard.objects.active()
    serializer_class = DebitCardsSerializer
    pagination_class = None
    http_method_names = ["retrieve", "get", "put", "delete"]

    def get_queryset(self):
        return super().get_queryset() \
            .filter(user=self.request.user) \
            .annotate(
                is_current=Case(
                    When(pk=self.request.user.current_debit_card_pk, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                )
            )


class TestPaymentRenderView(PublicAPIMixin, APIView):

    def get(self, request):
        return render(request, 'payments/create_payment.html')
