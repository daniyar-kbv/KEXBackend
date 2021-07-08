from rest_framework import serializers

from apps.orders.models.orders import RatedOrder, RateSample, RateStar
from apps.common.serializers import AbstractNameSerializer, AbstractTitleSerializer, AbstractDescriptionSerializer


class RateSampleSerializer(AbstractNameSerializer):
    class Meta:
        model = RateSample
        fields = ['id', 'name']
        extra_kwargs = {
            "name": {"required": False}
        }


class RateStarListSerializer(AbstractTitleSerializer, AbstractDescriptionSerializer):
    rate_samples = RateSampleSerializer(many=True)

    class Meta:
        model = RateStar
        fields = (
            "id",
            "value",
            "title",
            "description",
            "rate_samples",
        )


class RatedOrderListSerializer(serializers.ModelSerializer):
    rate_samples = RateSampleSerializer(many=True)

    class Meta:
        model = RatedOrder
        fields = (
            "star",
            "order",
            "comment",
            "rate_samples",
        )


class CreateRateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = RatedOrder
        fields = (
            "star",
            "order",
            "comment",
            "rate_samples"
        )
        extra_kwargs = {"rate_samples": {"required": False}}

    def create(self, validated_data):
        rating, _ = RatedOrder.objects.get_or_create(
            star=validated_data.get("star"),
            order=validated_data.get("order", None),
            comment=validated_data.get("comment"),
        )
        # print("validated_data: ", validated_data)
        if "rate_samples" in validated_data:
            rating.rate_samples.set(validated_data["rate_samples"])
        return rating
