from django.conf import settings
from django.contrib.auth import get_user_model

from apps.pipeline.instagram.exceptions import InstagramCodeInvalid, InstagramUnknownError
from apps.pipeline.instagram.integrations import InstagramCode
from apps.pipeline.instagram.integrations.base import GetAccessTokenByCode, GetUsername
from apps.promotions.models import Promotion, Participation

User = get_user_model()


def save_user_instagram(code: str, user_pk: int, promo_type: str, redirect_uri: str):
    access_token = GetAccessTokenByCode(instance=InstagramCode(code), redirect_uri=redirect_uri).run()

    if not access_token:
        raise InstagramCodeInvalid

    username = GetUsername(access_token=access_token).run()

    if not username:
        raise InstagramUnknownError

    user = User.objects.get(pk=user_pk)
    promotion = Promotion.objects.get(promo_type=promo_type)
    Participation.objects.create(
        user=user,
        promotion=promotion,
        instagram_username=username
    )


def get_instagram_auth_url(redirect_uri):
    url = f"https://api.instagram.com/oauth/authorize" \
          f"?client_id={settings.INSTAGRAM_CLIENT_ID}&" \
          f"redirect_uri={redirect_uri}" \
          f"&scope=user_profile,user_media&response_type=code"

    return url

