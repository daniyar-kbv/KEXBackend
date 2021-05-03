from rest_framework import serializers

from apps.partners.models import IIKOBrand, Organization


class OrganizationSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="outer_id", required=True)
    name = None


class UpdateBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = IIKOBrand
        fields = (
            ""
        )

