from rest_framework.generics import CreateAPIView

from apps.common.views import JSONRendererMixin

from .models import Payment
from .serializers import CreatePaymentSerializer


class CreatePaymentView(JSONRendererMixin, CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = CreatePaymentSerializer
