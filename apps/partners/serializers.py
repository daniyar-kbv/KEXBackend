from rest_framework import serializers

from .models import Brand, IIKOBrand


class BrandImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "name",
        )


class BrandAPILoginSerializer(serializers.ModelSerializer):
    images = BrandImagesSerializer(source="brand")
    name = serializers.CharField(source="brand.name")

    class Meta:
        model = IIKOBrand
        fields = (
            "id",
            "name",
            "images",
        )
