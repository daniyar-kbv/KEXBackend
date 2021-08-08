from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView

from apps.common.mixins import JSONPublicAPIMixin, JSONRendererMixin
from apps.notifications.models import FirebaseToken
from apps.notifications.serializers import CreateFirebaseTokenSerializer
from apps.orders.models import Order
from apps.promotions.models import Promotion


class CreateFirebaseTokenView(JSONPublicAPIMixin, CreateAPIView):
    queryset = FirebaseToken.objects.all()
    serializer_class = CreateFirebaseTokenSerializer


class AddUserToFirebaseTokenView(JSONRendererMixin, UpdateAPIView):
    queryset = FirebaseToken.objects.all()

    def get_object(self):
        return get_object_or_404(FirebaseToken, lead__uuid=self.kwargs.get("lead_uuid"))

    def update(self, request, *args, **kwargs):
        fbtoken = self.get_object()
        fbtoken.user = request.user
        fbtoken.save()

        return Response({})


class UpdateFirebaseTokenView(JSONRendererMixin, UpdateAPIView):
    queryset = FirebaseToken.objects.all()

    def get_object(self):
        return get_object_or_404(FirebaseToken, user=self.request.user)

    def update(self, request, *args, **kwargs):
        fbtoken = self.get_object()
        if not request.data.get('firebase_token'):
            raise ValueError("firebase_token key not provided")
        fbtoken.token = request.data.get('firebase_token')
        fbtoken.save()

        return Response({})


class OrderQuerysetView(JSONPublicAPIMixin, APIView):
    def get(self, request):
        return Response([{'id': o.id, 'name': str(o)} for o in Order.objects.all()], status.HTTP_200_OK)


class PromotionQuerysetView(JSONPublicAPIMixin, APIView):
    def get(self, request):
        return Response([{'id': p.id, 'name': str(p)} for p in Promotion.objects.all()], status.HTTP_200_OK)

