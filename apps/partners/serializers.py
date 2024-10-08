from rest_framework import serializers

from apps.common.serializers import AbstractNameSerializer
from apps.common import ImageTypes

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
    image = serializers.CharField(required=False)
    favicon = serializers.CharField(required=False)
    image_long = serializers.CharField(required=False)
    image_square = serializers.CharField(required=False)
    position = serializers.IntegerField()
    is_available = serializers.BooleanField(required=False)
    kml_map_url = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = (
            "id",
            "position",
            "name",
            "image",
            "favicon",
            "image_long",
            "image_square",
            "is_available",
            "kml_map_url",
        )

    def get_kml_map_url(self, brand):
        request = self.context.get('request')
        if brand.kml_map:
            kml_map_url = brand.kml_map.url
            return request.build_absolute_uri(kml_map_url)

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
        request = self.context.get("request")
        if request:
            image = obj.mobile_image_square if request.user_agent.is_mobile else obj.web_image_square
            if image:
                return request.build_absolute_uri(image.url)


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
                obj.brand.images.get(image_type=ImageTypes.IMAGE_SQUARE).image.url
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
            "img",
            "is_available"
        )

    def get_is_available(self, obj):
        city = self.context['city_id']
        if city:
            # print('obj: ', obj)
            if Branch.objects.filter(iiko_brand__brand=obj.brand, iiko_brand__city__id=city, is_active=True).exists():
                return True

        return False
