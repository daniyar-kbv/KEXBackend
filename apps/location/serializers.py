from rest_framework import serializers

from .models import Country, City


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "name", "country_code"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "name",


class CountryRetrieveSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, required=False)

    class Meta:
        model = Country
        fields = "name", "cities"
