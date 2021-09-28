from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    GenericAPIView,
)

from apps.common.mixins import PublicJSONRendererMixin, JSONRendererMixin
from apps.nomenclature.models import BranchPosition
from apps.payments.models import Payment
from apps.payments.serializers import CreatePaymentSerializer

from .decorators import check_branch_is_open, update_delivery_positions
from .exceptions import CouponNotActive
from .models import Order, Lead, Cart, Coupon
from .serializers import (
    ApplyLeadSerializer,
    AuthorizedApplySerializer,
    LeadNomenclatureSerializer,
    AdditionalNomenclaturePositionSerializer,
    BranchPositionSerializer,
    UpdateCartSerializer,
    LeadDetailSerializer,
    RetrieveCartSerializer,
    CreateOrderSerializer,
    OrdersListSerializer,
    CouponSerializer
)
from ..payments import PaymentStatusTypes


class LanguageToContextMixin:
    def get_serializer_context(self):
        return {
            "request": self.request,  # noqa
            "language": self.request.META["HTTP_LANGUAGE"],  # noqa
        }


class ApplyView(PublicJSONRendererMixin, CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = ApplyLeadSerializer


class AuthorizedApplyView(JSONRendererMixin, CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = AuthorizedApplySerializer


@method_decorator(update_delivery_positions, name='get')
class LeadShowView(PublicJSONRendererMixin, RetrieveAPIView):
    queryset = Lead.objects.all()
    lookup_field = "uuid"
    lookup_url_kwarg = "lead_uuid"
    serializer_class = LeadDetailSerializer


@method_decorator(check_branch_is_open, name="get")
@method_decorator(update_delivery_positions, name='get')
class LeadNomenclatureView(PublicJSONRendererMixin, LanguageToContextMixin, RetrieveAPIView):
    queryset = Lead.objects.all()
    lookup_field = "uuid"
    lookup_url_kwarg = "lead_uuid"
    serializer_class = LeadNomenclatureSerializer


@method_decorator(check_branch_is_open, name="get")
@method_decorator(update_delivery_positions, name='get')
class LeadNomenclatureRetrieveView(PublicJSONRendererMixin, LanguageToContextMixin, RetrieveAPIView):
    serializer_class = BranchPositionSerializer
    queryset = BranchPosition.objects.all()

    def get_object(self):
        return get_object_or_404(BranchPosition, uuid=self.kwargs["position_uuid"])


@method_decorator(check_branch_is_open, name="get")
@method_decorator(update_delivery_positions, name='get')
class LeadAdditionalNomenclatureView(PublicJSONRendererMixin, LanguageToContextMixin, ListAPIView):
    serializer_class = AdditionalNomenclaturePositionSerializer
    queryset = BranchPosition.objects.additional_positions()
    pagination_class = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lead'] = get_object_or_404(
            Lead.objects.select_related("cart"), uuid=self.kwargs.get('lead_uuid')
        )

        return context

    def get_queryset(self):
        lead = get_object_or_404(Lead, uuid=self.kwargs.get('lead_uuid'))
        return self.queryset.filter(
            branch_id=lead.branch_id,
        )


class OrdersListView(JSONRendererMixin, ListAPIView):
    queryset = Order.objects.select_related('lead', 'cart').prefetch_related('payments')\
        .filter(payments__status=PaymentStatusTypes.COMPLETED).order_by('-created_at')
    serializer_class = OrdersListSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


@method_decorator(check_branch_is_open, name="put")
@method_decorator(update_delivery_positions, name='put')
class UpdateCartView(PublicJSONRendererMixin, GenericAPIView):
    queryset = Cart.objects.all()
    serializer_class = UpdateCartSerializer

    def get_object(self):
        return get_object_or_404(
            Cart, lead__uuid=self.kwargs.get("lead_uuid")
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["branch"] = self.get_object().lead.branch

        return context

    @swagger_auto_schema(
        request_body=UpdateCartSerializer,
        responses={"200": RetrieveCartSerializer}
    )
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        output_serializer = RetrieveCartSerializer(instance)
        return Response(output_serializer.data)


class LastPaymentStatusView(JSONRendererMixin, RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = CreatePaymentSerializer

    def get_object(self):
        payments = Payment.objects.filter(order__lead_id=self.kwargs['lead_uuid'])
        if payments.exists():
            return payments.last()

        raise Http404


@method_decorator(check_branch_is_open, name="post")
class CreateOrderView(JSONRendererMixin, CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer


class CouponDetailView(PublicJSONRendererMixin, RetrieveAPIView):
    lookup_field = 'promocode'
    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()

    def get_object(self):
        obj = super().get_object()
        if obj:
            if not obj.is_active():
                raise CouponNotActive
        return obj
