from rest_framework import serializers

from .exceptions import FirebaseTokenDoesntExist
from .models import FirebaseToken
from .tasks import unregister_token_from_firebase


class CreateFirebaseTokenSerializer(serializers.ModelSerializer):
    firebase_token = serializers.CharField(source='token')

    class Meta:
        model = FirebaseToken
        fields = ('firebase_token',)

    def create(self, validated_data):
        print('firebase token create', validated_data['token'])
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
        fbtoken: FirebaseToken = FirebaseToken.objects.filter(
            token=self.data['firebase_token'],
            user=self.context.get('request').user
        ).first()
        unregister_token_from_firebase.delay(fbtoken.token)
        fbtoken.user = None
        fbtoken.save()
