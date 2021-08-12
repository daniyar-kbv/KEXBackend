from django.conf import settings
from django.contrib.auth import get_user_model

from apps.pipeline.instagram.exceptions import InstagramCodeInvalid, InstagramUnknownError
from apps.pipeline.instagram.integrations import InstagramCode
from apps.pipeline.instagram.integrations.base import GetAccessTokenByCode, GetUsername
from apps.promotions.models import Promotion, Participation
from apps.common.encryption import encrypt_user
User = get_user_model()


def get_instagram_username(code: str, user_pk: int, promo_type: str, redirect_uri: str):
    access_token = GetAccessTokenByCode(instance=InstagramCode(code), redirect_uri=redirect_uri).run()

    if not access_token:
        raise InstagramCodeInvalid

    username = GetUsername(access_token=access_token).run()

    if not username:
        raise InstagramUnknownError
    return username


def get_instagram_auth_url(request):
    url = f"https://api.instagram.com/oauth/authorize" \
          f"?client_id={settings.INSTAGRAM_CLIENT_ID}&" \
          f"redirect_uri={request.build_absolute_uri(request.path + f'instagram/{encrypt_user(request.user)}')}" \
          f"&scope=user_profile,user_media&response_type=code"

    return url

