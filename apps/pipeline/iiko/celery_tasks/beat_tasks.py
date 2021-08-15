from config import celery_app
from django.db.transaction import atomic

from apps.partners.models import LocalBrand
from ..integrations.branches import GetBranches
from ..integrations.nomenclature import GetLocalBrandNomenclature
from ..integrations.terminals import GetLocalBrandTerminals, CheckLocalBrandOrganizationsLiveness


@celery_app.task(name="iiko.update_brand_organizations")  # noqa
def update_brand_branches() -> None:
    for local_brand in LocalBrand.objects.active():
        with atomic():
            local_brand.deactivate_branches()
            GetBranches(instance=local_brand).run()
            GetLocalBrandTerminals(instance=local_brand).run()


@celery_app.task(name="iiko.update_brand_nomenclatures")  # noqa
def update_local_brands_nomenclatures():
    for local_brand in LocalBrand.objects.active():
        GetLocalBrandNomenclature(instance=local_brand).run()


@celery_app.task(name="iiko.check_brand_organizations_liveness")  # noqa
def check_brand_organizations_liveness() -> None:
    for local_brand in LocalBrand.objects.all():
        CheckLocalBrandOrganizationsLiveness(instance=local_brand).run()
