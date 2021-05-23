from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView

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
