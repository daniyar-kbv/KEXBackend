from rest_framework.generics import ListAPIView

from apps.common.mixins import JSONRendererMixin, PublicAPIMixin

from .models import BrandAPILogin
from .serializers import BrandAPILoginSerializer


class BrandImagesView(PublicAPIMixin, JSONRendererMixin, ListAPIView):
    queryset = BrandAPILogin.objects.all()
    serializer_class = BrandAPILoginSerializer

    def get_queryset(self):
        return self.queryset.filter(city=self.kwargs.get("city"))
