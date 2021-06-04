from config import celery_app

from apps.partners.models import LocalBrand
from apps.pipeline.iiko.integrations.auth import GetAuthToken


@celery_app.task(name="iiko.fetch_auth_token")
def fetch_auth_token(iiko_brand_pk: int):
    iiko_brand = LocalBrand.objects.get(
        pk=iiko_brand_pk
    )

    return GetAuthToken(instance=iiko_brand).run()
