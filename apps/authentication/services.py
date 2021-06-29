from django.conf import settings


def get_instagram_auth_url(request):
    url = f"https://api.instagram.com/oauth/authorize" \
          f"?client_id={settings.INSTAGRAM_CLIENT_ID}&" \
          f"redirect_uri={request.build_absolute_uri(settings.INSTAGRAM_REDIRECT_URI + request.kwargs.get('promo_type'))}" \
          f"&scope=user_profile,user_media&response_type=code"

    return url
