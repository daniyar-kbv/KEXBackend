from rest_framework.generics import CreateAPIView

from apps.common.mixins import PublicAPIMixin, JSONRendererMixin

from .serializers import ApplyLeadSerializer
from .models import Lead


class ApplyView(PublicAPIMixin, JSONRendererMixin, CreateAPIView):
    serializer_class = ApplyLeadSerializer
    queryset = Lead.objects.all()

    def perform_create(self, serializer):
        lead = serializer.save()
        print("created lead:", lead)
        # create service to find organization
        # test commit
        # test commit 2