from config import celery_app

from apps.partners.models import IIKOBrand
from apps.pipeline.iiko.integrations.auth import GetAuthToken


@celery_app.task
def fetch_auth_token(iiko_brand_pk: int):
    iiko_brand = IIKOBrand.objects.get(
        pk=iiko_brand_pk
    )

    return GetAuthToken(instance=iiko_brand).run()
