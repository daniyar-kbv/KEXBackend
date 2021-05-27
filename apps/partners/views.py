from rest_framework.generics import ListAPIView

from apps.common.mixins import JSONRendererMixin, PublicAPIMixin

from .models import IIKOBrand
from .serializers import BrandAPILoginSerializer


class BrandListView(PublicAPIMixin, JSONRendererMixin, ListAPIView):
    queryset = IIKOBrand.objects.all()
    serializer_class = BrandAPILoginSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'city_id': self.kwargs.get("city_id", None)
        }

    def get_queryset(self):
        city = self.kwargs.get("city_id")
        if city:
            return self.queryset.filter(city=city)

        return self.queryset.distinct("brand")
