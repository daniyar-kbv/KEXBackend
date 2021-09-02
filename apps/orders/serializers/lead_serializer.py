from rest_framework import serializers

from apps.location.models import Address
from apps.location.serializers import AddressSerializer
from apps.orders.models import Cart, Lead
from apps.partners.models import LocalBrand
from apps.partners.exceptions import BrandNotFound
from apps.nomenclature.models import (
    BranchCategory,
    BranchPosition,
)

from .retrieve_cart_serializers import RetrieveCartSerializer

from ..exceptions import (
    UserHasNoAddressError,
)


class LeadAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "city",
            "longitude",
            "latitude",
            "district",
            "street",
            "building",
            "corpus",
            "flat",
            "comment",
        )

    extra_kwargs = {
        "longitude": {"required": True},
        "latitude": {"required": True},
        "city": {"required": True},
    }


class AuthorizedApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = "uuid",
        extra_kwargs = {"read_only": True}

    def validate(self, attrs):
        if not self.context["request"].user.addresses.exists():
            raise UserHasNoAddressError

        return super().validate(attrs)

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        validated_data["address"] = user.current_address.address
        validated_data["local_brand"] = user.current_address.local_brand

        lead = super().create(validated_data)

        if lead.cart is None:
            lead.cart = Cart.objects.create()
            lead.save(update_fields=["cart"])

        return lead


class ApplyLeadSerializer(serializers.ModelSerializer):
    address = LeadAddressSerializer(write_only=True, required=True)

    class Meta:
        model = Lead
        fields = (
            "uuid",
            "address",
            "local_brand",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "local_brand": {"write_only": True}
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if not attrs["local_brand"].city == attrs["address"]["city"]:
            raise BrandNotFound

        # for testing
        # attrs["local_brand"] = LocalBrand.objects.active().first()

        return attrs

    def create(self, validated_data):
        validated_data["address"] = Address.objects.create(  # noqa
            **validated_data.pop("address")
        )
        lead = super().create(validated_data)

        if lead.cart is None:
            lead.cart = Cart.objects.create()
            lead.save(update_fields=["cart"])

        return lead


class AuthorizedApplyWithAddressSerializer(ApplyLeadSerializer):
    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        lead = super().create(validated_data)
        user.add_new_address(lead.address, lead.local_brand)

        return lead


class LeadDetailSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)
    brand_name = serializers.SerializerMethodField(required=False)
    brand_image = serializers.SerializerMethodField(required=False)
    cart = RetrieveCartSerializer(required=False)

    class Meta:
        model = Lead
        fields = (
            "cart",
            "uuid",
            "address",
            "brand_name",
            "brand_image",
        )

    def get_brand_name(self, obj):
        try:
            return obj.local_brand.brand.name.text_ru
        except Exception as exc:
            return None

    def get_brand_image(self, obj):
        from apps.partners import BrandImageTypes

        request = self.context["request"]
        image = obj.local_brand.brand.images.filter(image_type=BrandImageTypes.IMAGE_SQUARE).first()

        if image is not None:
            return request.build_absolute_uri(image.image.url)


class AdditionalNomenclaturePositionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    category = serializers.UUIDField(source="branch_category_id")

    class Meta:
        model = BranchPosition
        fields = (
            "uuid",
            "name",
            "price",
            "description",
            "image",
            "count",
            "is_available",
            "category",
        )

    def get_count(self, obj):
        cart = self.context['lead'].cart
        return cart.get_count_for_given_position(str(obj.uuid))

    def get_name(self, obj):
        if not obj.name:
            return

        return obj.name.text(lang=self.context["language"])

    def get_description(self, obj):
        if not obj.description:
            return

        return obj.description.text(lang=self.context["language"])

    def get_image(self, obj):
        if not obj.position.image:
            return

        request = self.context["request"]
        return request.build_absolute_uri(obj.position.image.url)


class NomenclaturePositionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    category = serializers.UUIDField(source="branch_category_id")

    class Meta:
        model = BranchPosition
        fields = (
            "uuid",
            "name",
            "price",
            "description",
            "image",
            "is_available",
            "category",
        )

    def get_name(self, obj):
        if not obj.name:
            return

        return obj.name.text(lang=self.context["language"])

    def get_description(self, obj):
        if not obj.description:
            return

        return obj.description.text(lang=self.context["language"])

    def get_image(self, obj):
        if not obj.position.image:
            return

        request = self.context["request"]
        return request.build_absolute_uri(obj.position.image.url)


class NomenclatureCategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    positions = NomenclaturePositionSerializer(source="branch_positions.main_positions", many=True)

    class Meta:
        model = BranchCategory
        fields = (
            "name",
            "uuid",
            "positions",
        )

    def get_name(self, obj):
        if not obj.name:
            return

        return obj.name.text(lang=self.context["language"])


class LeadNomenclatureSerializer(serializers.ModelSerializer):
    categories = NomenclatureCategorySerializer(source="branch.branch_categories.active", many=True, read_only=True)

    class Meta:
        model = Lead
        fields = (
            "uuid",
            "categories",
        )
