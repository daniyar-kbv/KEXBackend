"""
Only for cron, not for import
"""

from config import celery_app
from django.db.transaction import atomic

from apps.partners.models import IIKOBrand
from ..integrations.organizations import GetOrganizations


@celery_app.task(name="iiko.update_brand_organizations")  # noqa
def update_brand_organizations():
    for brand in IIKOBrand.objects.active():
        with atomic():
            brand.deactivate_organizations()
            GetOrganizations(instance=brand).run()
