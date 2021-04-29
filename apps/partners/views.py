from rest_framework.generics import ListAPIView

from apps.common.mixins import JSONRendererMixin, PublicAPIMixin

from .models import IIKOBrand
from .serializers import BrandAPILoginSerializer


class BrandImagesView(PublicAPIMixin, JSONRendererMixin, ListAPIView):
    queryset = IIKOBrand.objects.all()
    serializer_class = BrandAPILoginSerializer

    def get_queryset(self):
        return self.queryset.filter(city=self.kwargs.get("city"))
