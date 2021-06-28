from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
)

from apps.common.mixins import JSONPublicAPIMixin
from apps.nomenclature.models import BranchPosition
from apps.pipeline.iiko.celery_tasks.branches import find_lead_organization

from .models import Lead, Cart
from .serializers import (
    ApplyLeadSerializer,
    LeadNomenclatureSerializer,
    BranchPositionSerializer,
    UpdateCartSerializer,
)


class ApplyView(JSONPublicAPIMixin, CreateAPIView):
    serializer_class = ApplyLeadSerializer
    queryset = Lead.objects.all()  # noqa

    def perform_create(self, serializer):
        lead = serializer.save()

        # for testing
        lead.branch = lead.local_brand.branches.first()
        lead.save(update_fields=["branch"])

        # find_lead_organization(lead_pk=lead.pk)


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


class CartRetrieveUpdateView(JSONPublicAPIMixin, RetrieveUpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = UpdateCartSerializer

    def get_object(self):
        return get_object_or_404(Cart, lead__uuid=self.kwargs.get("lead_uuid"))
