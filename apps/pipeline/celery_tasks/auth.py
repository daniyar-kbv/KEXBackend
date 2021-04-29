from config import celery_app

from apps.partners.models import BrandAPILogin
from apps.pipeline.integrations.iiko_integrations.auth import GetAuthToken


@celery_app.task
def fetch_auth_token(brand_api_login_pk: int):
    brand_api_login = BrandAPILogin.objects.get(
        pk=brand_api_login_pk
    )

    return GetAuthToken(instance=brand_api_login).run()
