"""
Only for cron, not for import
"""

from config import celery_app
from django.db.transaction import atomic

from apps.partners.models import LocalBrand, Branch
from ..integrations.organizations import GetOrganizations
from ..integrations.nomenclature import GetOrganizationNomenclature


@celery_app.task(name="iiko.update_brand_organizations")  # noqa
def update_brand_organizations() -> None:
    """
    Update organizations of all brands
    :return:
    """

    for brand in LocalBrand.objects.active():
        with atomic():
            brand.deactivate_organizations()
            GetOrganizations(instance=brand).run()


@celery_app.task(name="iiko.update_brand_nomenclatures") # noqa
def update_brand_nomenclatures():
    """
    Update nomenclatures of all brands
    :return:
    """

    for branch in Branch.objects.active():
        GetOrganizationNomenclature(instance=branch).run()
