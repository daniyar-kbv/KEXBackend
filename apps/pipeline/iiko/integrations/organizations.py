from typing import Any, TYPE_CHECKING

from .base import BaseIIKOService

from .serializers import (
    IIKOOrganizationSerializer,
    IIKOLeadOrganizationSerializer,
)

if TYPE_CHECKING:
    from apps.orders.models import Lead


class GetOrganizations(BaseIIKOService):
    """Получение списка организации"""
    endpoint = "api/1/organizations"
    save_serializer = IIKOOrganizationSerializer

    def run_service(self) -> Any:
        return self.fetch(json={
                "returnAdditionalInfo": True,
        })

    @staticmethod
    def parse_address(full_address=None):
        try:
            district, city, street_with_building = full_address.split(', ')
            street, building = street_with_building.split()
        except (ValueError, AttributeError):
            return {}

        return {
            "city": city,
            "district": district,
            "street": street,
            "building": building,
        }

    def prepare_to_save(self, data: dict) -> list:
        prepared_data = list()
        for org in data["organizations"]:
            prepared_data.append({
                "iiko_brand": self.instance.pk,  # noqa
                "name": org.get("name"),
                "outer_id": org.get("id"),
                "address": {
                    "country": org.get("country"),
                    "longitude": org.get("longitude"),
                    "latitude": org.get("latitude"),
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
    endpoint = "api/1/delivery_restrictions/allowed"
    save_serializer = IIKOLeadOrganizationSerializer
    instance: 'Lead' = None

    def __init__(self, instance=None, **kwargs):
        super().__init__(instance, **kwargs)
        self.random_organization_id = str(self.instance.iiko_brand.organizations.first().outer_id)
        self.longitude = str(self.instance.address.longitude)
        self.latitude = str(self.instance.address.latitude)

    def get_iiko_brand_pk(self):
        return self.instance.iiko_brand_id  # noqa

    def run_service(self) -> Any:
        return self.fetch(json={
            "organizationId": self.random_organization_id,
            "isCourierDelivery": True,
            "orderLocation": {
                "latitude": self.latitude,
                "longitude": self.longitude,
            }
        })

    def prepare_to_save(self, data: dict) -> dict:
        allowed_items = data.get("allowedItems")[0]

        if not data.get("isAllowed") or allowed_items is None:
            print('1', not data.get("isAllowed"))
            print('2', allowed_items is None)
            return {}

        return {
            "order_zone": allowed_items.get("zone"),
            "organization_outer_id": allowed_items.get("organizationId"),
            "estimated_duration": allowed_items.get("deliveryDurationInMinutes"),
        }

    def finalize_response(self, response) -> bool:
        return response.get("isAllowed", False)
