from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    GenericAPIView,
)

from apps.common.mixins import JSONPublicAPIMixin
from apps.pipeline.iiko.celery_tasks.organizations import find_lead_organization

from .serializers import ApplyLeadSerializer, LeadNomenclatureSerializer
from .models import Lead


class ApplyView(JSONPublicAPIMixin, CreateAPIView):
    serializer_class = ApplyLeadSerializer
    queryset = Lead.objects.all()  # noqa

    def perform_create(self, serializer):
        lead = serializer.save()
        find_lead_organization(lead_pk=lead.pk)


class LeadNomenclatureView(JSONPublicAPIMixin, RetrieveAPIView):
    serializer_class = LeadNomenclatureSerializer
    queryset = Lead.objects.all()
    lookup_field = "uuid"
    lookup_url_kwarg = "lead_uuid"

from .models import CartPosition
from .serializers import UpdateCartSerializer
from rest_framework.response import Response

class UpdateCartView(JSONPublicAPIMixin, APIView):
    def post(self, request, lead_uuid, *args, **kwargs):
        lead = get_object_or_404(Lead, uuid=lead_uuid)
        serializer = UpdateCartSerializer(
            instance=lead.cart,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)


class IncrementCartPositionView(JSONPublicAPIMixin, APIView):
    def post(self, request, lead_uuid, position_uuid, *args, **kwargs):
        lead = get_object_or_404(Lead, uuid=lead_uuid)
        position: CartPosition = get_object_or_404(
            CartPosition,
            cart_id=lead.cart_id,
            position_id=position_uuid,
        )

        position.increment_count()

        return Response()


class DecrementCartPositionView(JSONPublicAPIMixin, APIView):
    def post(self, request, lead_uuid, position_uuid, *args, **kwargs):
        lead = get_object_or_404(Lead, uuid=lead_uuid)
        position: CartPosition = get_object_or_404(
            CartPosition,
            cart_id=lead.cart_id,
            position_id=position_uuid,
        )

        position.decrement_count()

        return Response()
