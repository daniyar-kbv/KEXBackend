from rest_framework import serializers

from apps.location.models import Address
from apps.partners.models import IIKOBrand
from apps.partners.exceptions import BrandNotFound

from .models import Lead


class LeadAddressSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField(required=True)
    latitude = serializers.CharField(required=True)

    class Meta:
        model = Address
        fields = "__all__"


class ApplyLeadSerializer(serializers.ModelSerializer):
    address = LeadAddressSerializer(write_only=True)
    city_pk = serializers.CharField(required=True, write_only=True)
    brand_pk = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Lead
        fields = (
            "uuid",
            "city_pk",
            "address",
            "brand_pk",
        )
        extra_kwargs = {
            "uuid": {"read_only": True}
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        city_pk, brand_pk = attrs.pop("city_pk"), attrs.pop("brand_pk")

        if not IIKOBrand.objects.filter(brand_id=brand_pk, city_id=city_pk).exists():
            raise BrandNotFound

        attrs["iiko_brand"] = IIKOBrand.objects.get(brand_id=brand_pk, city_id=city_pk)

        return attrs

    def create(self, validated_data):
        print('validated_data is', validated_data)
        validated_data["address"], created = Address.objects.get_or_create(  # noqa
            **validated_data.pop("address")
        )

        return super().create(validated_data)
