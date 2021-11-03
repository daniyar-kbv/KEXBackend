from config import celery_app

from apps.partners.models import LocalBrand
from apps.pipeline.iiko.integrations.auth import GetAuthToken


@celery_app.task(name="iiko.fetch_auth_token")
def fetch_auth_token(iiko_brand_pk: int):
    local_brand = LocalBrand.objects.get(
        pk=iiko_brand_pk
    )

    return GetAuthToken(instance=local_brand).run()


def remove_auth_token(iiko_brand_pk: int):
    local_brand = LocalBrand.objects.get(
        pk=iiko_brand_pk
    )

    GetAuthToken.remove_from_cache(local_brand)
