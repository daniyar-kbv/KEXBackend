from rest_framework import serializers
from django.shortcuts import get_object_or_404

from apps.orders.models import Lead
from apps.location.models import Address
from apps.location.serializers import AddressSerializer
from apps.partners.exceptions import BrandNotFound
from apps.nomenclature.models import BranchPosition, Category
from apps.pipeline.iiko import ApplyTypes
from apps.pipeline.iiko.celery_tasks.branches import find_lead_organization

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
    address = LeadAddressSerializer(write_only=True, required=False)
    user_address = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Lead
        fields = (
            "uuid",
            "address",
            "user_address",
            "local_brand",
        )
        extra_kwargs = {
            "uuid": {"read_only": True},
            "local_brand": {"write_only": True, "required": False},
        }

    def set_change_type(self, attrs) -> str:
        address = attrs.get('address')
        local_brand = attrs.get('local_brand')
        user = attrs['user']

        if address:
            if not local_brand or not local_brand.city == address['city']:
                raise BrandNotFound

            comment = address.pop('comment', None)
            address_queryset = Address.objects.filter(
                id__in=user.addresses.values_list('address_id', flat=True), **address,
            )

            if address_queryset.exists():
                db_address = address_queryset.first()
                db_address.comment = comment or db_address.comment
                db_address.save(update_fields=['comment'])
                attrs['address'] = db_address
                attrs['change_type'] = ApplyTypes.EXISTING_NEW_USER_ADDRESS.value
            else:
                attrs['address'] = Address.objects.create(**address, comment=comment)
                attrs['change_type'] = ApplyTypes.NEW_USER_ADDRESS.value

        elif attrs.get('user_address'):
            if not attrs['user'].addresses.exists():
                raise UserHasNoAddressError

            user_address = get_object_or_404(user.addresses.all(), id=attrs.pop('user_address'))
            attrs['address'] = user_address.address

            if local_brand:
                attrs['change_type'] = ApplyTypes.CHANGE_USER_ADDRESS_BRAND.value
            else:
                attrs['local_brand'] = user_address.local_brand
                attrs['change_type'] = ApplyTypes.SWITCH_BETWEEN_USER_ADDRESSES.value

        else:
            if not attrs['user'].addresses.exists():
                raise UserHasNoAddressError

            current_address = attrs['user'].current_address
            attrs['address'] = current_address.address
            attrs['local_brand'] = current_address.local_brand
            attrs['change_type'] = ApplyTypes.CURRENT_ADDRESS.value

        return attrs

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs['user'] = self.context['request'].user

        self.set_change_type(attrs)

        return attrs

    def create(self, validated_data):
        print('AuthorizedApplySerializer (validated_data):', validated_data)
        change_type = validated_data.pop('change_type', None)
        lead = super().create(validated_data)
        find_lead_organization(lead.id, change_type)

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

        return attrs

    def create(self, validated_data):
        validated_data["address"] = Address.objects.create(  # noqa
            **validated_data.pop("address")
        )
        lead = super().create(validated_data)
        find_lead_organization(lead.id)

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
        request = self.context.get("request")
        if request:
            image = obj.local_brand.brand.mobile_image_square if request.user_agent.is_mobile else obj.local_brand.brand.web_image_square
            if image:
                return request.build_absolute_uri(image.url)


class LeadCheckSerializer(serializers.ModelSerializer):
    brand_name = serializers.SerializerMethodField(required=False)
    brand_image = serializers.SerializerMethodField(required=False)
    cart = RetrieveCartSerializer(required=False)

    class Meta:
        model = Lead
        fields = (
            "cart",
            "brand_name",
            "brand_image",
        )

    def get_brand_name(self, obj):
        try:
            return obj.local_brand.brand.name.text_ru
        except Exception as exc:
            return None

    def get_brand_image(self, obj):
        from apps.common import ImageTypes

        request = self.context["request"]
        image = obj.local_brand.brand.images.filter(image_type=ImageTypes.IMAGE_FOR_CHECK).first()

        if image is not None:
            return request.build_absolute_uri(image.image.url)


class AdditionalNomenclaturePositionSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    category = serializers.UUIDField(source="branch_category_id", required=False)

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

    def get_image(self, obj):
        request = self.context.get("request")
        if request:
            image = obj.position.mobile_image if request.user_agent.is_mobile else obj.position.web_image
            if image:
                return request.build_absolute_uri(image.url)


class NomenclaturePositionSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category = serializers.UUIDField(source="category_id")

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

    def get_image(self, obj):
        request = self.context.get("request")
        if request:
            image = obj.position.mobile_image if request.user_agent.is_mobile else obj.position.web_image
            if image:
                return request.build_absolute_uri(image.url)


class NomenclatureCategorySerializer(serializers.ModelSerializer):
    positions = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            "name",
            "uuid",
            "positions",
        )

    def get_positions(self, obj):
        lead: Lead = self.context['lead']

        return NomenclaturePositionSerializer(
            instance=lead.branch.branch_positions.main_positions().filter(category_id=obj.uuid),
            context=self.context,
            many=True,
        ).data


class LeadNomenclatureSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = (
            "uuid",
            "categories",
        )

    def get_categories(self, obj):
        return NomenclatureCategorySerializer(
            instance=obj.local_brand.categories.active(),
            context={**self.context, 'lead': obj},
            many=True,
        ).data
