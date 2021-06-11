from rest_framework import serializers

from apps.common.serializers import AbstractImageSerializer
from apps.promotions.models import Promotion


class PromotionListSerializer(AbstractImageSerializer):
    link = serializers.CharField(required=False)

    class Meta:
        model = Promotion
        fields = [
            'position',
            'id',
            'type',
            'image',
            'slug',
            'link',
        ]
