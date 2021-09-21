from rest_framework import serializers


class AbstractNameSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        abstract = True

    def get_name(self, obj):
        try:
            language = self.context['request'].headers.get('language')
        except Exception:
            language = "ru"

        return getattr(obj.name, language)


class AbstractTitleSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        abstract = True

    def get_title(self, obj):
        return getattr(obj.title, self.context['request'].headers.get('language'))


class AbstractDescriptionSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        abstract = True

    def get_description(self, obj):
        return getattr(obj.description, self.context['request'].headers.get('language'))


class AbstractImageSerializer(serializers.ModelSerializer):
    image_small = serializers.SerializerMethodField(source='image')
    image_big = serializers.SerializerMethodField()

    class Meta:
        abstract = True

    def get_image_small(self, obj):
        if obj.image:
            image = getattr(obj.image, self.context['request'].headers.get('language'))
            if image:
                return self.context['request'].build_absolute_uri(image.url)
        return None

    def get_image_big(self, obj):
        if obj.image_big:
            image = getattr(obj.image_big, self.context['request'].headers.get('language'))
            if image:
                return self.context['request'].build_absolute_uri(image.url)
        return None
