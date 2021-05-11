from typing import TYPE_CHECKING

from .base import BaseIIKOService

if TYPE_CHECKING:
    from apps.partners.models import Organization


class GetOrganizationNomenclature(BaseIIKOService):
    """Получение меню организации"""
    endpoint = "/api/1/nomenclature"
    instance: 'Organization' = None
    save_serializer = None

    def get_iiko_brand_pk(self):
        return self.instance.iiko_brand_id  # noqa

    def run_service(self):
        return self.fetch(json={
            "organizationId": str(self.instance.outer_id)
        })

    def finalize_response(self, response):
        return self.clean_empty(response)

    def clean_empty(self, d):
        if isinstance(d, dict):
            return {
                k: v
                for k, v in ((k, self.clean_empty(v)) for k, v in d.items())
                if v
            }
        if isinstance(d, list):
            return [v for v in map(self.clean_empty, d) if v]
        return d
