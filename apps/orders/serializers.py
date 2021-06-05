from rest_framework import serializers

from apps.location.models import Address
from apps.partners.models import LocalBrand, Branch
from apps.partners.exceptions import BrandNotFound
from apps.nomenclature.models import BranchCategory, BranchPosition

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

        if not LocalBrand.objects.filter(brand_id=brand_id, city_id=city_id).exists():
            raise BrandNotFound

        attrs["local_brand"] = LocalBrand.objects.get(brand_id=brand_id, city_id=brand_id)

        return attrs

    def create(self, validated_data):
        print('validated_data is', validated_data)
        validated_data["address"], created = Address.objects.get_or_create(  # noqa
            **validated_data.pop("address")
        )

        return super().create(validated_data)


class NomenclatureCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchCategory
        fields = (
            "name",
            "uuid"
        )


class NomenclaturePositionSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(source="position.iiko_name")
    # description = serializers.CharField(source="position.iiko_description")
    # category = serializers.CharField(source="position.category_id")
    # outer_id = serializers.CharField(source="local_position.outer_id")
    image = serializers.SerializerMethodField()

    class Meta:
        model = BranchPosition
        fields = (
            "id",
            "name",
            "description",
            "image",
            # "description",
            "price",
            "branch_category",
        )

    def get_image(self, obj):
        if not obj.local_position.image:
            return

        request = self.context["request"]
        return request.build_absolute_uri(obj.local_position.image.url)


class LeadNomenclatureSerializer(serializers.ModelSerializer):
    categories = NomenclatureCategorySerializer(source="branch_categories", many=True, read_only=True)
    positions = NomenclaturePositionSerializer(source="branch_positions", many=True, read_only=True)

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

    def to_representation(self, instance):
        # todo: add select relates
        data = super().to_representation(instance)
        data["categories"] = NomenclatureCategorySerializer(
            instance=instance.branch.branch_categories.filter(
                name__isnull=False,
                is_active=True,
            ),
            many=True, context=self.context,
        ).data
        data["positions"] = NomenclaturePositionSerializer(
            instance=instance.branch.branch_positions.filter(
                branch_category__isnull=False,
                name__isnull=False,
            ),
            many=True, context=self.context,
        ).data

        return data


from apps.orders.models import Cart, CartPosition


class UpdatePositionSerializer(serializers.ModelSerializer):
    position_uuid = serializers.UUIDField(required=True)

    class Meta:
        model = CartPosition
        fields = (
            "position_uuid",
            "count",
            "comment",
        )


class UpdateCartSerializer(serializers.ModelSerializer):
    cart_positions = UpdatePositionSerializer(many=True, required=True)

    class Meta:
        model = Cart
        fields = "cart_positions",

    def update(self, instance, validated_data):
        for cart_position in validated_data["cart_positions"]:
            instance.cart_positions.update_or_create(
                organization_position_id=cart_position.pop("position_uuid"),
                defaults={**cart_position}
            )

        return instance
