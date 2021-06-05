from rest_framework import serializers

from apps.common.serializers import AbstractNameSerializer

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
    image = serializers.CharField(required=False)
    is_available = serializers.BooleanField(required=False)

    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
            "image",
            "is_available"
        )


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
