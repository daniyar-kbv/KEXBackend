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
        FirebaseToken.objects.filter(token=validated_data['token']).delete()
        FirebaseToken.objects.filter(user=validated_data.get('user')).delete()

        fbtoken = FirebaseToken.objects.create(
            token=validated_data['token'],
            user= validated_data.get("user"),
        )
        return fbtoken


class FirebaseTokenSerializer(serializers.ModelSerializer):
    firebase_token = serializers.CharField(source='token')

    class Meta:
        model = FirebaseToken
        fields = ('firebase_token',)

    def delete_user(self):
        fbtoken: FirebaseToken = FirebaseToken.objects.filter(
            token=self.data['firebase_token'],
            user=self.context.get('request').user
        ).first()
        if fbtoken:
            unregister_token_from_firebase.delay(fbtoken.token)
            fbtoken.delete()
