from typing import Any, Dict, TYPE_CHECKING, Optional, List

from apps.partners.exceptions import TerminalNotFound

from .base import BaseIIKOService

from .serializers import (
    IIKOOrganizationSerializer,
    IIKOLeadOrganizationSerializer,
)

if TYPE_CHECKING:
    from apps.orders.models import Lead


class GetBranches(BaseIIKOService):
    """Получение списка организации"""
    endpoint = "api/1/organizations"
    save_serializer = IIKOOrganizationSerializer

    def run_service(self) -> Any:
        return self.fetch(json={
            "returnAdditionalInfo": True,
        })

    def parse_address(self, full_address=None):
        try:
            district, city, street_with_building = full_address.split(', ')
            street, building = street_with_building.split()
        except (ValueError, AttributeError):
            return {}

        return {
            "district": district,
            "street": street,
            "building": building,
        }

    def prepare_to_save(self, data: dict) -> list:
        prepared_data = list()
        for org in data["organizations"]:
            prepared_data.append({
                "local_brand": self.instance.pk,  # noqa
                "iiko_name": org.get("name"),
                "outer_id": org.get("id"),
                "address": {
                    # "country": self.instance.country_id,
                    "longitude": org.get("longitude"),
                    "latitude": org.get("latitude"),
                    "city": self.instance.city_id,
                    **self.parse_address(org.get("restaurantAddress")),
                },
            })

        return prepared_data

    def finalize_response(self, response):
        return None

    def save(self, prepared_data):
        serializer = self.save_serializer(
            data=self.prepare_to_save(prepared_data), many=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()


class FindOrganization(BaseIIKOService):
    """Поиск наиболее подходящего терминала"""
    endpoint = "api/1/delivery_restrictions/allowed"
    save_serializer = IIKOLeadOrganizationSerializer
    instance: 'Lead' = None

    def get_local_brand_pk(self):
        return self.instance.local_brand_id  # noqa

    def run_service(self) -> Any:
        return self.fetch(json={
            "organizationId": str(self.instance.local_brand.branches.first().outer_id),
            "isCourierDelivery": True,
            "orderLocation": {
                "latitude": str(self.instance.address.latitude),
                "longitude": str(self.instance.address.longitude),
            }
        })

    def prepare_to_save(self, prepared_data) -> Optional[List[Dict]]:
        if not prepared_data or not prepared_data.get('allowedItems') or not prepared_data.get('isAllowed'):
            return

        organizations = []

        for allowed_item in prepared_data.get('allowedItems'):
            organizations.append(self.get_organization_info(allowed_item))

        return organizations

    def get_organization_info(self, allowed_item):
        branch = self.instance.local_brand.branches\
            .prefetch_related('delivery_times')\
            .get(outer_id=allowed_item['organizationId'])

        return {
            'branch': branch.pk,
            'is_open': branch.delivery_times.open().exists(),
            'change_type': self.kwargs.get('change_type'),
            'order_zone': allowed_item['zone'],
            'estimated_duration': allowed_item['deliveryDurationInMinutes']
        }

    def save(self, prepared_data):
        ...

    def finalize_response(self, response):
        prepared_data = self.prepare_to_save(response)

        if not prepared_data:
            raise TerminalNotFound

        serializer = self.save_serializer(
            instance=self.instance,
            data=sorted(prepared_data, key=lambda x: x['is_open'])[0],
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
