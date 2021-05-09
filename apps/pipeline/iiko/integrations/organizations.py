from typing import Any

from .base import BaseIIKOService

from .serializers import IIKOOrganizationSerializer


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
                "iiko_brand": self.instance.pk,
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
