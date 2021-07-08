from rest_framework import serializers

from apps.location.models import Address
from apps.partners.models import LocalBrand
from apps.partners.exceptions import BrandNotFound
from apps.orders.models import (
    Cart,
    CartPosition,
    CartPositionModifier,
    CartPositionModifierGroup,
)
from apps.nomenclature.models import (
    BranchCategory,
    BranchPosition,
    ModifierGroup,
    BranchPositionModifier,
)

from .models import Lead
from .models.orders import RatedOrder, RateSample, RateStar
from apps.common.serializers import AbstractNameSerializer, AbstractTitleSerializer, AbstractDescriptionSerializer


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
        )

    extra_kwargs = {
        "longitude": {"required": True},
        "latitude": {"required": True},
        "city": {"required": True},
    }


class ApplyLeadSerializer(serializers.ModelSerializer):
    address = LeadAddressSerializer(write_only=True, required=True)

    class Meta:
        model = Lead
        fields = (
            "uuid",
            "address",
        )
        extra_kwargs = {
            "uuid": {"read_only": True}
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if not attrs["local_brand"].city == attrs["address"]["city"]:
            raise BrandNotFound

        # for testing
        attrs["local_brand"] = LocalBrand.objects.active().first()

        return attrs

    def create(self, validated_data):
        validated_data["address"], created = Address.objects.get_or_create(  # noqa
            **validated_data.pop("address")
        )
        lead = super().create(validated_data)

        if lead.cart is None:
            lead.cart = Cart.objects.create()
            lead.save(update_fields=["cart"])

        return lead


class LeadDetailSerializer(serializers.ModelSerializer):
    address = LeadAddressSerializer(required=False)
    brand_name = serializers.SerializerMethodField(required=False)
    brand_image = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Lead
        fields = (
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


class NomenclatureCategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = BranchCategory
        fields = (
            "name",
            "uuid"
        )

    def get_name(self, obj):
        if not obj.name:
            return

        return obj.name.text(lang=self.context["language"])


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


class ModifierSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(source="modifier.uuid")
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = BranchPositionModifier
        fields = (
            "uuid",
            "name",
            "image",
        )

    def get_name(self, obj):
        if not obj.modifier.name:
            return

        return obj.modifier.name.text(lang=self.context["language"])

    def get_image(self, obj):
        if not obj.modifier.local_position.image:
            return

        return self.context["request"].build_absolute_uri(
            obj.modifier.local_position.image.url
        )


class ModifierGroupSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    modifiers = ModifierSerializer(many=True, required=False)

    class Meta:
        model = ModifierGroup
        fields = (
            "uuid",
            "name",
            "modifiers",
            "min_amount",
            "max_amount",
            "is_required",
        )

    def get_name(self, obj):
        if not obj.name:
            return

        return obj.name.text(lang=self.context["language"])


class BranchPositionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    modifier_groups = ModifierGroupSerializer(many=True, required=False)

    class Meta:
        model = BranchPosition
        fields = (
            "uuid",
            "name",
            "description",
            "image",
            "price",
            "branch_category",
            "modifier_groups",
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
        if not obj.local_position.image:
            return

        request = self.context["request"]
        return request.build_absolute_uri(obj.local_position.image.url)


# Cart Serializers
class BranchPositionShortSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    category = serializers.UUIDField(source="branch_category_id", read_only=True)

    class Meta:
        model = BranchPosition
        fields = (
            "uuid",
            "name",
            "image",
            "price",
            "category",
        )
        extra_kwargs = {
            "price": {"read_only": True}
        }

    def get_name(self, obj):
        if not obj.name:
            return

        return obj.name.text(lang=self.context.get("language", "ru"))

    def get_image(self, obj):
        if not obj.local_position.image:
            return

        request = self.context["request"]
        return request.build_absolute_uri(obj.local_position.image.url)


class CartPositionModifierSerializer(serializers.ModelSerializer):
    # position_uuid = serializers.UUIDField(required=True, write_only=True)
    position = BranchPositionShortSerializer(source="branch_position") #, read_only=True)

    class Meta:
        model = CartPositionModifier
        fields = (
            "position",
            #"position_uuid",
            "count",
        )


class CartPositionModifierGroupSerializer(serializers.ModelSerializer):
    group_uuid = serializers.UUIDField(required=True, write_only=True)
    modifiers = CartPositionModifierSerializer(many=True, required=False)

    class Meta:
        model = CartPositionModifierGroup
        fields = (
            "group_uuid",
            "modifiers",
        )


class CartPositionSerializer(serializers.ModelSerializer):
    position = serializers.UUIDField(required=True, write_only=True)
    #position = BranchPositionShortSerializer(source="branch_position")#, read_only=True)
    modifier_groups = CartPositionModifierGroupSerializer(many=True, required=False)

    class Meta:
        model = CartPosition
        fields = (
            "position",
            "count",
            "position",
            "comment",
            #"modifiers",
            "modifier_groups",
        )


class UpdateCartSerializer(serializers.ModelSerializer):
    positions = CartPositionSerializer(many=True, required=False)

    class Meta:
        model = Cart
        fields = (
            "positions",
        )

    def update(self, instance, validated_data):
        positions = validated_data.pop("positions")

        for position in positions:
            print("position is", position)
            cart_position, created = instance.positions.update_or_create(
                branch_position_id=position["position_uuid"],
                defaults={
                    "comment": position["comment"],
                    "count": position["count"],
                }
            )

            for modifier in position.get("modifiers", list()):
                cart_position.modifiers.update_or_create(
                    branch_position_id=modifier["position_uuid"],
                    defaults={
                        "count": modifier["count"],
                    }
                )

        return instance
