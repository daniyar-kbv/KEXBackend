from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, UpdateAPIView

from apps.common.views import JSONRendererMixin

from .models import Payment, DebitCard
from .serializers import (
    DebitCardsSerializer,
    CreatePaymentSerializer,
    CreateCardPaymentSerializer,
    Confirm3DSPaymentSerializer,
)


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


class DebitCardsListViewSet(
    JSONRendererMixin,
    ModelViewSet,
):
    lookup_field = "uuid"
    queryset = DebitCard.objects.all()
    serializer_class = DebitCardsSerializer
    http_method_names = ["retrieve", "get", "put", "delete"]

    def get_queryset(self):
        return self.request.user.get_all_debit_cards
