from django.conf import settings
from django.contrib.auth import get_user_model

from apps.pipeline.instagram.exceptions import InstagramCodeInvalid, InstagramUnknownError
from apps.pipeline.instagram.integrations import InstagramCode, InstagramAccessToken
from apps.pipeline.instagram.integrations.base import GetAccessTokenByCode, GetUsername
from apps.promotions.models import Promotion, Participation

User = get_user_model()


def get_instagram_username(code: str, promo_type: str):
    access_token = GetAccessTokenByCode(
        instance=InstagramCode(code),
        redirect_uri=get_promotion(promo_type).web_url
    ).run()

    if not access_token:
        raise InstagramCodeInvalid

    username = GetUsername(instance=InstagramAccessToken(access_token)).run()

    if not username:
        raise InstagramUnknownError
    return username


def get_instagram_auth_url(promo_type):
    url = f"{settings.INSTAGRAM_VERIFICATION_URI}" \
          f"?client_id={settings.INSTAGRAM_CLIENT_ID}&" \
          f"redirect_uri={promo_type}" \
          f"&scope=user_profile,user_media&response_type=code"

    return url


def save_participation_in_promotion(user, promo_type, username):
    Participation.objects.update_or_create(
        promotion=get_promotion(promo_type),
        instagram_username=username,
        user=user,
    )


def is_participant(user, promo_type):
    return Participation.objects.filter(
        user=user,
        promotion=get_promotion(promo_type)
    ).exists()


def get_promotion(promo_type):
    print(promo_type)
    print(Promotion.objects.get(promo_type=promo_type.upper()))
    print(Promotion.objects.get(promo_type=promo_type.upper()).web_url)
    return Promotion.objects.get(promo_type=promo_type.upper())
