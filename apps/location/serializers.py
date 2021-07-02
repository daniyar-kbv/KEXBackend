from rest_framework import serializers

from .models import Country, City
from ..common.serializers import AbstractNameSerializer


class CountrySerializer(AbstractNameSerializer):
    class Meta:
        model = Country
        fields = "id", "name", "country_code"


class CitySerializer(AbstractNameSerializer):
    class Meta:
        model = City
        fields = "id", "name", "latitude", "longitude"


class CityRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "name", "country"


class CountryRetrieveSerializer(AbstractNameSerializer):
    cities = CitySerializer(many=True, required=False)

    class Meta:
        model = Country
        fields = "name", "cities"
