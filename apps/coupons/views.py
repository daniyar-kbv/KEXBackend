from rest_framework.generics import RetrieveAPIView

from apps.common.mixins import PublicJSONRendererMixin

from .models import Coupon
from .serializers import CouponSerializer
from .exceptions import CouponNotActive


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
