from rest_framework import serializers

from apps.common.serializers import AbstractNameSerializer
from . import BrandImageTypes

from .models import Brand, LocalBrand, Branch


class BrandImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            # "name",
            "image_square",
            "image_short",
            "image_tall",
            "image_long",
        )


class BrandSerializer(AbstractNameSerializer):
    id = serializers.SerializerMethodField()
    image_small = serializers.CharField(required=False)
    image_big = serializers.CharField(required=False)
    position = serializers.IntegerField()
    is_available = serializers.BooleanField(required=False)

    class Meta:
        model = Brand
        fields = (
            "id",
            "position",
            "name",
            "image_small",
            "image_big",
            "is_available"
        )

    def get_id(self, obj):
        local_brand = obj.local_brands.filter(city_id=self.context["city_id"]).first()
        if local_brand is not None:
            return local_brand.id


class SquareImageBrandSerializer(AbstractNameSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
            "image"
        )

    def get_image(self, obj):
        img_file = obj.images.filter(image_type=BrandImageTypes.IMAGE_SQUARE).first()
        if img_file:
            return self.context['request'].build_absolute_uri(img_file.image.url)
        return None


class UserLocalBrandsSerializer(AbstractNameSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = LocalBrand
        fields = (
            'id',
            'name',
            'image',
        )

    def get_image(self, obj):
        try:
            return self.context['request'].build_absolute_uri(
                obj.brand.images.get(image_type=BrandImageTypes.IMAGE_SQUARE).image.url
            )
        except:
            ...


class BrandAPILoginSerializer(serializers.ModelSerializer):
    images = BrandImagesSerializer(source="brand")
    name = serializers.CharField(source="brand.name")
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = LocalBrand
        fields = (
            "id",
            "name",
            "images",
            "is_available"
        )

    def get_is_available(self, obj):
        city = self.context['city_id']
        if city:
            print('obj: ', obj)
            if Branch.objects.filter(iiko_brand__brand=obj.brand, iiko_brand__city__id=city, is_active=True).exists():
                return True

        return False
