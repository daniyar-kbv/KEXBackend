from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.views import APIView

from apps.common.views import JSONRendererMixin

from .models import Payment, DebitCard
from .serializers import (
    DebitCardsSerializer,
    CreatePaymentSerializer,
    CreateCardPaymentSerializer,
    Confirm3DSPaymentSerializer,
)
from apps.common.mixins import PublicAPIMixin


class CreatePaymentView(JSONRendererMixin, CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = CreatePaymentSerializer


class CreateCardPaymentView(JSONRendererMixin, CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = CreateCardPaymentSerializer


class Confirm3DSPaymentView(JSONRendererMixin, UpdateAPIView):
    allowed_methods = ["PUT"]
    queryset = Payment.objects.all()
    serializer_class = Confirm3DSPaymentSerializer
    lookup_field = "uuid"
    lookup_url_kwarg = "payment_uuid"


class DebitCardsListView(JSONRendererMixin, ListAPIView):
    queryset = DebitCard.objects.is_active()
    serializer_class = DebitCardsSerializer

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user
        )


class TestPaymentRenderView(PublicAPIMixin, APIView):

    def get(self, request):
        return render(request, 'payments/create_payment.html')
