from rest_framework import serializers

# from .models import TestCountry


class AbstractNameSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        abstract = True

    def get_name(self, obj):
        return getattr(obj.name, self.context['request'].headers.get('language'))


# class TestCountrySerializer(AbstractNameSerializer):
#     extra = serializers.SerializerMethodField()
#
#     class Meta:
#         model = TestCountry
#         fields = ("id", "name", "extra")
#
#     def get_extra(self, obj):
#         return obj.extra.text(self.context['request'].headers.get('language'))
