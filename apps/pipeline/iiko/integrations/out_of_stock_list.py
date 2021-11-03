from typing import TYPE_CHECKING

from django.core.cache import cache
from django.db.transaction import atomic

from apps.partners.models import Branch
from .base import BaseIIKOService

if TYPE_CHECKING:
    from apps.partners.models import LocalBrand


class GetBrandOutOfStockList(BaseIIKOService):
    """Получение стоп листа филила"""
    endpoint = "/api/1/stop_lists"
    instance: 'LocalBrand' = None

    def get_local_brand_pk(self):  # noqa
        return self.instance.pk

    def get_branches_list(self):
        return [str(i) for i in self.instance.branches.active().values_list('outer_id', flat=True)]

    def run_service(self):
        return self.fetch(json={
            "organizationIds": self.get_branches_list()
        })

    def prepare_to_save(self, data: dict):
        prepared_data = []
        for branch in data.get('terminalGroupStopLists', []):
            try:
                organizations = []
                for k in branch['items']:
                    for i in k['items']:
                        organizations.append(i['productId'])
                prepared_data.append({
                    branch['organizationId']: organizations
                })
            except Exception as exc:
                print(f'Error while update out of stock list: {exc}')
                continue
        return prepared_data

    @atomic
    def update_organization_out_of_stock_list(self, data):
        branch_outer_id = list(data.keys())[0]
        branch = Branch.objects.get(outer_id=branch_outer_id, local_brand=self.instance)
        branch.branch_positions.filter(position__outer_id__in=data[branch_outer_id]).update(is_available=False)
        branch.branch_positions.exclude(position__outer_id__in=data[branch_outer_id]).update(is_available=True)

    def finalize_response(self, response):
        ...

    def save(self, prepared_data):
        prepared_data = self.prepare_to_save(prepared_data)
        for data in prepared_data:
            self.update_organization_out_of_stock_list(data)
