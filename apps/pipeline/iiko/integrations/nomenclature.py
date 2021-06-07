from decimal import Decimal
from typing import TYPE_CHECKING, Optional, List, Dict

from ..python_entities.positions import (
    Modifier as PythonModifier,
    Position as PythonPosition,
)

from .serializers import IIKONomenclatureSerializer
from .base import BaseIIKOService

if TYPE_CHECKING:
    from apps.partners.models import Branch


class GetBranchNomenclature(BaseIIKOService):
    """Получение меню организации"""
    endpoint = "/api/1/nomenclature"
    instance: 'Branch' = None
    save_serializer = IIKONomenclatureSerializer

    def get_local_brand_pk(self):
        return self.instance.local_brand_id  # noqa

    def run_service(self):
        return self.fetch(json={
            "organizationId": str(self.instance.outer_id)
        })

    @staticmethod
    def _fetch_price(position: Dict) -> Decimal:
        unavailable_price = Decimal("0.00")

        if position.get("sizePrices") is not None and isinstance(position["sizePrices"], list):
            price = position["sizePrices"][0]\
                .get("price", {})\
                .get("currentPrice", unavailable_price)

            return Decimal(price)

        return unavailable_price

    @staticmethod
    def _fetch_modifiers(position: Dict) -> List[Optional[PythonModifier]]:
        modifiers: List[Dict] = list()

        for modifier in position.get("modifiers", list()):
            modifiers.append(PythonModifier(
                outer_id=modifier.get("id"),
                min_amount=modifier.get("min_amount"),
                max_amount=modifier.get("max_amount"),
                required=modifier.get("required"),
            ).__dict__)

        return modifiers or None

    def prepare_to_save(self, data: dict) -> List:
        positions: List[Dict] = list()

        for position in data.get("products", list()):
            positions.append(PythonPosition(
                outer_id=position.get('id'),
                local_brand=self.instance.local_brand_id,  # noqa
                iiko_name=position.get("name") or None,
                iiko_description=position.get("description") or None,
                price=self._fetch_price(position),
                modifiers=self._fetch_modifiers(position),
            ).__dict__)

        return positions

    def finalize_response(self, response):
        return None

    def save(self, prepared_data):
        # print("prepared_data", self.prepare_to_save(prepared_data))
        serializer = self.save_serializer(
            data=self.prepare_to_save(prepared_data), many=True,
            context={"branch": self.instance}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
