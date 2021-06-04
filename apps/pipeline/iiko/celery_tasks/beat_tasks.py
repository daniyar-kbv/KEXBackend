"""
Only for cron, not for import
"""

from config import celery_app
from django.db.transaction import atomic

from apps.partners.models import LocalBrand, Branch
from ..integrations.branches import GetBranches
from ..integrations.nomenclature import GetOrganizationNomenclature


@celery_app.task(name="iiko.update_brand_organizations")  # noqa
def update_brand_branches() -> None:
    """
    Update branches of all brands
    :return:
    """

    for brand in LocalBrand.objects.active():
        with atomic():
            brand.deactivate_branches()
            GetBranches(instance=brand).run()


@celery_app.task(name="iiko.update_brand_nomenclatures") # noqa
def update_brand_nomenclatures():
    """
    Update nomenclatures of all brands
    :return:
    """

    for branch in Branch.objects.active():
        GetOrganizationNomenclature(instance=branch).run()
