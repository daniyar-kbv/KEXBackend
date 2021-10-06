from django.urls import reverse
from rest_framework import serializers

from apps.common.serializers import AbstractNameSerializer

from .models import Document


class DocumentListSerializer(AbstractNameSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            'priority',
            'id',
            'name',
            'slug',
            'link',
        ]

    def get_link(self, obj):
        request = self.context["request"]
        return request.build_absolute_uri(reverse(
            "documents:render-by-slug",
            args=[obj.slug]
        ))
