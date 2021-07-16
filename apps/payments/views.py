from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView

from apps.common.views import JSONRendererMixin

from .models import Payment, DebitCard
from .serializers import (
    DebitCardsSerializer,
    CreatePaymentSerializer,
    Confirm3DSPaymentSerializer,
)


class CreatePaymentView(JSONRendererMixin, CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = CreatePaymentSerializer


class CreateCardPaymentView(JSONRendererMixin, CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = None


class Confirm3DSPaymentView(JSONRendererMixin, UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = Confirm3DSPaymentSerializer
    lookup_field = "uuid"


class DebitCardsListView(JSONRendererMixin, ListAPIView):
    queryset = DebitCard.objects.is_active()
    serializer_class = DebitCardsSerializer

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user
        )
