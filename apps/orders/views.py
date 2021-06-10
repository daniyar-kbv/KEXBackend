from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    GenericAPIView,
)

from apps.common.mixins import JSONPublicAPIMixin
from apps.nomenclature.models import BranchPosition
from apps.pipeline.iiko.celery_tasks.branches import find_lead_organization

from .serializers import ApplyLeadSerializer, LeadNomenclatureSerializer, BranchPositionSerializer
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

    def get_serializer_context(self):
        return {
            "request": self.request,
            "language": self.request.META["HTTP_LANGUAGE"],
        }


class BranchPositionView(JSONPublicAPIMixin, RetrieveAPIView):
    serializer_class = BranchPositionSerializer
    queryset = BranchPosition.objects.all()

    def get_object(self):
        print("kwargs:", self.kwargs)
        return get_object_or_404(BranchPosition, uuid=self.kwargs["position_uuid"])

    def get_serializer_context(self):
        return {
            "request": self.request,
            "language": self.request.META["HTTP_LANGUAGE"],
        }


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
