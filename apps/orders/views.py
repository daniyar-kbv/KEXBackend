from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    RetrieveAPIView,
)

from apps.common.mixins import JSONPublicAPIMixin, JSONRendererMixin
from apps.nomenclature.models import BranchPosition
from apps.pipeline.iiko.celery_tasks.branches import find_lead_organization

from .models import Order, Lead, Cart
from .models.orders import RateStar
from .serializers import (
    ApplyLeadSerializer,
    AuthorizedApplySerializer,
    LeadNomenclatureSerializer,
    BranchPositionSerializer,
    UpdateCartSerializer,
    LeadDetailSerializer,
    RetrieveCartSerializer,
    RatedOrderListSerializer,
    RateStarListSerializer,
    CreateRateOrderSerializer,
    CreateOrderSerializer,
    OrdersListSerializer,
)


class BaseApplyView(CreateAPIView):
    def perform_create(self, serializer):
        lead = serializer.save()

        # for testing
        lead.branch = lead.local_brand.branches.first()
        lead.save(update_fields=["branch"])

        # find_lead_organization(lead_pk=lead.pk)


class ApplyView(JSONPublicAPIMixin, BaseApplyView):
    serializer_class = ApplyLeadSerializer
    queryset = Lead.objects.all()


class AuthorizedApplyView(JSONRendererMixin, BaseApplyView):
    serializer_class = AuthorizedApplySerializer
    queryset = Lead.objects.all()


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


class OrdersListView(JSONRendererMixin, ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrdersListSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CreateOrderView(JSONRendererMixin, CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer


class RateStarListView(JSONPublicAPIMixin, ListAPIView):
    queryset = RateStar.objects.all()
    serializer_class = RateStarListSerializer


class CreateRateOrderView(JSONPublicAPIMixin, CreateAPIView):
    serializer_class = CreateRateOrderSerializer
