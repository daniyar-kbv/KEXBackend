from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView

from apps.common.mixins import PublicJSONRendererMixin
from .models import RateStar
from .serializers import CreateRateOrderSerializer, RateStarListSerializer


class RateStarListView(PublicJSONRendererMixin, ListAPIView):
    queryset = RateStar.objects.all()
    serializer_class = RateStarListSerializer
    pagination_class = None


class CreateRateOrderView(PublicJSONRendererMixin, CreateAPIView):
    serializer_class = CreateRateOrderSerializer
