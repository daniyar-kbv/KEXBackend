from rest_framework.generics import CreateAPIView, ListAPIView

from apps.common.views import JSONRendererMixin

from .models import Payment, DebitCard
from .serializers import CreatePaymentSerializer, DebitCardsSerializer


class CreatePaymentView(JSONRendererMixin, CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = CreatePaymentSerializer


class DebitCardsListView(JSONRendererMixin, ListAPIView):
    queryset = DebitCard.objects.is_active()
    serializer_class = DebitCardsSerializer

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user
        )
