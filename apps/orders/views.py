from rest_framework.generics import CreateAPIView

from apps.partners.exceptions import TerminalNotFound
from apps.common.mixins import PublicAPIMixin, JSONRendererMixin
from apps.pipeline.iiko.celery_tasks.organizations import find_lead_organization

from .serializers import ApplyLeadSerializer
from .models import Lead


class ApplyView(PublicAPIMixin, JSONRendererMixin, CreateAPIView):
    serializer_class = ApplyLeadSerializer
    queryset = Lead.objects.all()  # noqa

    def perform_create(self, serializer):
        lead = serializer.save()

        is_found = find_lead_organization(lead_pk=lead.pk)

        if not is_found:
            raise TerminalNotFound
