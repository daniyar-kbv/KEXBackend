from rest_framework import serializers

# from .models import TestCountry


class AbstractNameSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        abstract = True

    def get_name(self, obj):
        return getattr(obj.name, self.context['request'].headers.get('language'))


class AbstractDescriptionSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        abstract = True

    def get_description(self, obj):
        return getattr(obj.name, self.context['request'].headers.get('language'))
