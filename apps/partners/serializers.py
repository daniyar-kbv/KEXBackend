from rest_framework import serializers

from .models import Brand, IIKOBrand, Organization


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


class BrandAPILoginSerializer(serializers.ModelSerializer):
    images = BrandImagesSerializer(source="brand")
    name = serializers.CharField(source="brand.name")
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = IIKOBrand
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
            if Organization.objects.filter(iiko_brand__brand=obj.brand, iiko_brand__city__id=city, is_active=True).exists():
                return True
        return False
