from rest_framework import serializers

from apps.common.serializers import AbstractImageSerializer, AbstractNameSerializer, AbstractDescriptionSerializer
from apps.promotions.models import Promotion, Participation


class PromotionListSerializer(AbstractNameSerializer, AbstractImageSerializer, AbstractDescriptionSerializer):
    link = serializers.CharField(required=False)

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


# class ParticipationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Participation
#         fields = [
#             'user': {
#                 'user',
#                 'insta'
#             }
#         ]
