from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.common.mixins import JSONRendererMixin

from .models import Country
from .serializers import CountrySerializer, CountryRetrieveSerializer


class CountryViewSet(JSONRendererMixin, ReadOnlyModelViewSet):
    queryset = Country.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CountryRetrieveSerializer

        return CountrySerializer
