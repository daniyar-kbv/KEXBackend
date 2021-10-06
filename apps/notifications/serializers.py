from rest_framework import serializers

from apps.notifications.exceptions import FirebaseTokenDoesntExist
from apps.notifications.models import FirebaseToken
from apps.orders.models import Lead


class CreateFirebaseTokenSerializer(serializers.ModelSerializer):
    firebase_token = serializers.CharField(source='token')

    class Meta:
        model = FirebaseToken
        fields = ('firebase_token',)

    def create(self, validated_data):
        fbtoken, _ = FirebaseToken.objects.update_or_create(
            token=validated_data['token'],
            defaults={
                "user": validated_data.get("user")
            }
        )
        return fbtoken


class FirebaseTokenSerializer(serializers.ModelSerializer):
    firebase_token = serializers.CharField(source='token')

    class Meta:
        model = FirebaseToken
        fields = ('firebase_token',)

    def validate(self, attrs):
        if not FirebaseToken.objects.filter(token=attrs['token'], user=self.context.get('request').user).exists():
            raise FirebaseTokenDoesntExist
        return attrs

    def delete_user(self):
        fbtoken = FirebaseToken.objects.filter(
            token=self.data['firebase_token'],
            user=self.context.get('request').user
        ).first()
        fbtoken.user = None
        fbtoken.save()
