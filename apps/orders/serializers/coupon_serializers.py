from rest_framework import serializers

from apps.orders.models.orders import Coupon


class CouponSerializer(serializers.ModelSerializer):
    group = serializers.SlugField()
    description = serializers.SlugField()

    class Meta:
        model = Coupon
        fields = (
            'group',
            'promocode',
            'description',
            'start_date',
            'end_date'
        )
