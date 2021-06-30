from rest_framework import serializers

from apps.common.serializers import AbstractImageSerializer, AbstractNameSerializer
from apps.promotions.models import Promotion, Participation


class PromotionListSerializer(AbstractNameSerializer, AbstractImageSerializer):
    link = serializers.CharField(required=False)

    class Meta:
        model = Promotion
        fields = [
            'priority',
            'id',
            'name',
            'type',
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
