from rest_framework import serializers

from apps.common.serializers import AbstractImageSerializer, AbstractNameSerializer, AbstractDescriptionSerializer
from apps.promotions.models import Promotion, Participation


class PromotionListSerializer(AbstractNameSerializer, AbstractDescriptionSerializer):
    link = serializers.CharField(required=False)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = [
            'priority',
            'id',
            'promo_type',
            'name',
            'description',
            'image',
            'slug',
            'link',
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if request:
            image = obj.mobile_image if request.user_agent.is_mobile else obj.web_image
            if image:
                image = getattr(image, request.headers.get('language'))
            if image:
                return request.build_absolute_uri(image.url)
