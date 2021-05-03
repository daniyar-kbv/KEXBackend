from rest_framework import serializers

from apps.partners.models import IIKOBrand, Organization


class OrganizationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="outer_id", required=True)

    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
        )


class UpdateBrandSerializer(serializers.ModelSerializer):
    organizations = OrganizationSerializer(many=True, required=True)

    class Meta:
        model = IIKOBrand
        fields = "organizations",

    def update(self, instance, validated_data):
        for organization_data in validated_data.pop("organizations"):
            Organization.objects.get_or_create(
                outer_id=organization_data["outer_id"],
                defaults={
                    "is_active": True,
                    "iiko_brand": instance,
                    "name": organization_data["name"],
                },
            )

        return instance
