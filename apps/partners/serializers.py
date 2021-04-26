from rest_framework import serializers

from .models import Brand, BrandAPILogin


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
        model = BrandAPILogin
        fields = (
            "id",
            "name",
            "images",
        )
