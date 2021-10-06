from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.common.mixins import JSONRendererMixin, PublicAPIMixin

from .models import Country, City
from .serializers import CountrySerializer, CountryRetrieveSerializer, CitySerializer


class CountryViewSet(PublicAPIMixin, JSONRendererMixin, ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CountryRetrieveSerializer

        return CountrySerializer


class CityViewSet(PublicAPIMixin, JSONRendererMixin, ReadOnlyModelViewSet):
    queryset = City.objects.all()
    pagination_class = None

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CitySerializer

        return CitySerializer
