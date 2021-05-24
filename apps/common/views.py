from rest_framework.generics import ListAPIView

from apps.common.mixins import JSONRendererMixin, PublicAPIMixin

# from .models import TestCountry
# from .serializers import TestCountrySerializer


# class TestCountryView(PublicAPIMixin, JSONRendererMixin, ListAPIView):
#     queryset = TestCountry.objects.all() \
#         .select_related("name", "extra")
#
#     serializer_class = TestCountrySerializer
