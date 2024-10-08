from config import celery_app
from django.db.transaction import atomic

from apps.partners.models import LocalBrand

from ..integrations.branches import GetBranches
from ..integrations.branch_zones import GetBranchZones
from ..integrations.nomenclature import GetLocalBrandNomenclature, GetBranchNomenclaturePrices
from ..integrations.terminals import GetLocalBrandTerminals, CheckLocalBrandOrganizationsLiveness
from ..integrations.out_of_stock_list import GetBrandOutOfStockList
from ..integrations.payments import GetPayments
from ..integrations.cancel_causes import GetCancelCauses


@celery_app.task(name="iiko.update_brand_organizations")  # noqa
def update_brand_branches() -> None:
    for local_brand in LocalBrand.objects.all():
        with atomic():
            local_brand.deactivate_branches()
            GetBranches(instance=local_brand).run()
            GetLocalBrandTerminals(instance=local_brand).run()
            CheckLocalBrandOrganizationsLiveness(instance=local_brand).run()


@celery_app.task(name="iiko.update_brand_nomenclatures")  # noqa
def update_local_brands_nomenclatures():
    for local_brand in LocalBrand.objects.all():
        with atomic():
            GetLocalBrandNomenclature(instance=local_brand).run()
            for branch in local_brand.branches.all():
                GetBranchNomenclaturePrices(instance=branch).run()


@celery_app.task(name="iiko.update_brand_payments")
def update_brand_payments() -> None:
    for local_brand in LocalBrand.objects.all():
        GetPayments(local_brand).run()


@celery_app.task(name='iiko.update_out_of_stock_list')
def update_out_of_stock_list() -> None:
    for local_brand in LocalBrand.objects.active():
        GetBrandOutOfStockList(local_brand).run()


@celery_app.task(name='iiko.update_brand_cancel_causes')
def update_brand_cancel_causes() -> None:
    for local_brand in LocalBrand.objects.all():
        GetCancelCauses(local_brand).run()


@celery_app.task(name='iiko.update_branch_zones')
def update_branch_zones() -> None:
    for locals_brand in LocalBrand.objects.all():
        GetBranchZones(locals_brand).run()
