from rest_framework import serializers

from apps.location.models import Address
from apps.partners.models import IIKOBrand
from apps.partners.exceptions import BrandNotFound
from apps.nomenclature.models import Category, PositionInfoByOrganization

from .models import Lead


class LeadAddressSerializer(serializers.ModelSerializer):
    longitude = serializers.CharField(required=True)
    latitude = serializers.CharField(required=True)

    class Meta:
        model = Address
        fields = "__all__"


class ApplyLeadSerializer(serializers.ModelSerializer):
    address = LeadAddressSerializer(write_only=True)
    city_id = serializers.CharField(required=True, write_only=True)
    brand_id = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Lead
        fields = (
            "uuid",
            "brand_id",
            "city_id",
            "address",
        )
        extra_kwargs = {
            "uuid": {"read_only": True}
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        city_id, brand_id = attrs.pop("city_id"), attrs.pop("brand_id")

        if not IIKOBrand.objects.filter(brand_id=brand_id, city_id=city_id).exists():
            raise BrandNotFound

        attrs["iiko_brand"] = IIKOBrand.objects.get(brand_id=brand_id, city_id=brand_id)

        return attrs

    def create(self, validated_data):
        print('validated_data is', validated_data)
        validated_data["address"], created = Address.objects.get_or_create(  # noqa
            **validated_data.pop("address")
        )

        return super().create(validated_data)


class NomenclatureCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "uuid"
        )


class NomenclaturePositionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="position.iiko_name")
    description = serializers.CharField(source="position.iiko_description")
    category = serializers.CharField(source="position.category_id")

    class Meta:
        model = PositionInfoByOrganization
        fields = (
            "name",
            "description",
            "price",
            "category",
        )


class LeadNomenclatureSerializer(serializers.ModelSerializer):
    categories = NomenclatureCategorySerializer(source="brand.categories", many=True, read_only=True)
    positions = NomenclaturePositionSerializer(source="organization.positions", many=True, read_only=True)

    class Meta:
        model = Lead
        fields = (
            "uuid",
            "categories",
            "positions",
        )
        extra_kwargs = {
            "uuid": {"read_only": True}
        }
