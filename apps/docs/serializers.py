from rest_framework import serializers

from .models import Document
from apps.common.serializers import AbstractNameSerializer


class DocumentListSerializer(AbstractNameSerializer):
    link = serializers.CharField(required=False)

    class Meta:
        model = Document
        fields = [
            'priority',
            'id',
            'name',
            'slug',
            'link',
        ]