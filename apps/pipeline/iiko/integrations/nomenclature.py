from decimal import Decimal
from typing import TYPE_CHECKING, List, Dict

from ..python_entities.positions import (
    Modifier as PythonModifier,
    Position as PythonPosition,
    SizePrice as PythonSizePrice,
)

from .base import BaseIIKOService
from .serializers import IIKONomenclatureSerializer, IIKOPositionSizeSerializer

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
    def _fetch_size_prices(position: Dict) -> List[Dict]:
        size_prices = []

        for size_price in position.get("sizePrices", list()):
            size_prices.append(PythonSizePrice(
                outer_id=size_price["sizeId"],
                price=size_price.get("price", {}).get("currentPrice")
            ).__dict__)

        print("size_prices:", size_prices)
        return size_prices

    @staticmethod
    def _fetch_modifiers(position) -> List[Dict]:
        modifiers: List[Dict] = list()

        for modifier in position.get("modifiers", list()):
            modifiers.append(PythonModifier(
                outer_id=modifier.get("id"),
                min_amount=modifier.get("min_amount") or 1,
                max_amount=modifier.get("max_amount") or 1,
                required=modifier.get("required") or False,
            ).__dict__)

        return modifiers or None

    @staticmethod
    def sort_positions(positions):
        return sorted(
            positions,
            key=lambda x: bool(x.get('modifiers'))
        )

    @staticmethod
    def save_position_sizes(position_sizes):
        serializer = IIKOPositionSizeSerializer(data=position_sizes, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def prepare_to_save(self, data: dict) -> List:
        positions: List[Dict] = list()
        position_sizes = data.get("sizes")

        if position_sizes:
            self.save_position_sizes(position_sizes)

        for position in data.get("products", list()):
            positions.append(PythonPosition(
                outer_id=position.get('id'),
                local_brand=self.instance.local_brand_id,  # noqa
                iiko_name=position.get("name") or None,
                iiko_description=position.get("description") or None,
                size_prices=self._fetch_size_prices(position), # noqa
                modifiers=self._fetch_modifiers(position), # noqa
            ).__dict__)

        return self.sort_positions(positions)

    def finalize_response(self, response):
        return None

    def save(self, prepared_data):
        serializer = self.save_serializer(
            data=self.prepare_to_save(prepared_data), many=True,
            context={"branch": self.instance}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
