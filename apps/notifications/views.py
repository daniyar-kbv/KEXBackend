from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView

from apps.common.mixins import PublicJSONRendererMixin, JSONRendererMixin
from apps.notifications.models import FirebaseToken
from apps.notifications.serializers import CreateFirebaseTokenSerializer
from apps.orders.models import Order
from apps.promotions.models import Promotion


class FirebaseTokenSaveView(PublicJSONRendererMixin, CreateAPIView):
    queryset = FirebaseToken.objects.all()
    serializer_class = CreateFirebaseTokenSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user if self.request.user.is_authenticated else None)


class FirebaseTokenUpdateView(PublicJSONRendererMixin, UpdateAPIView):
    queryset = FirebaseToken.objects.all()

    def get_object(self):
        return get_object_or_404(FirebaseToken, token=self.request.data.get("old_firebase_token"))

    def update(self, request, *args, **kwargs):
        fbtoken = self.get_object()
        if request.user.is_authenticated:
            fbtoken.user = request.user
        fbtoken.token = request.data.get('new_firebase_token')
        fbtoken.save()

        return Response({})


class OrderQuerysetView(PublicJSONRendererMixin, APIView):
    def get(self, request):
        return Response([{'id': o.id, 'name': str(o)} for o in Order.objects.all()], status.HTTP_200_OK)


class PromotionQuerysetView(PublicJSONRendererMixin, APIView):
    def get(self, request):
        return Response([{'id': p.id, 'name': str(p)} for p in Promotion.objects.all()], status.HTTP_200_OK)
