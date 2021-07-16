from rest_framework import serializers

from apps.notifications.models import FirebaseToken
from apps.orders.models import Lead


class CreateFirebaseTokenSerializer(serializers.ModelSerializer):
    lead_uuid = serializers.UUIDField(source='lead')
    firebase_token = serializers.CharField(source='token')

    class Meta:
        model = FirebaseToken
        fields = ('firebase_token', 'lead_uuid')

    def create(self, validated_data):
        fbtoken, _ = FirebaseToken.objects.update_or_create(
            lead=Lead.objects.get(uuid=validated_data.get("lead")),
            defaults={
                "token": validated_data.get("token")
            }
        )
        return fbtoken
