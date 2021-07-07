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
    LeadDetailSerializer,
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


class LeadShowView(JSONPublicAPIMixin, RetrieveAPIView):
    serializer_class = LeadDetailSerializer
    queryset = Lead.objects.all()
    lookup_field = "uuid"
    lookup_url_kwarg = "lead_uuid"


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

from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from .serializers import RetrieveCartSerializer
class CartRetrieveUpdateView(JSONPublicAPIMixin, UpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = UpdateCartSerializer

    def get_object(self):
        return get_object_or_404(Cart, lead__uuid=self.kwargs.get("lead_uuid"))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        output_serializer = RetrieveCartSerializer(instance)
        # output_serializer.is_valid(raise_exception=True)
        return Response(output_serializer.data)
