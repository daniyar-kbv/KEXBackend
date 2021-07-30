from rest_framework import serializers

from .models import Country, City, Address
from ..common.serializers import AbstractNameSerializer


class CountrySerializer(AbstractNameSerializer):
    class Meta:
        model = Country
        fields = "id", "name", "country_code"


class CitySerializer(AbstractNameSerializer):
    class Meta:
        model = City
        fields = "id", "name", "latitude", "longitude"


class AddressSerializer(serializers.ModelSerializer):
    country = CountrySerializer(source="city.country")
    city = CitySerializer()

    class Meta:
        model = Address
        fields = (
            "country",
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


class CityRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "name", "country"


class CountryRetrieveSerializer(AbstractNameSerializer):
    cities = CitySerializer(many=True, required=False)

    class Meta:
        model = Country
        fields = "name", "cities"
