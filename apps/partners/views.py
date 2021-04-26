from rest_framework.generics import ListAPIView

from apps.common.mixins import JSONRendererMixin, PublicAPIMixin

from .models import Brand
from .serializers import BrandImagesSerializer


class BrandImagesView(PublicAPIMixin, JSONRendererMixin, ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandImagesSerializer

    def get_queryset(self):
        return self.queryset.filter(api_logins__city=self.kwargs.get("city"))
