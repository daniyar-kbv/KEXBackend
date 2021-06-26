from decimal import Decimal
from typing import TYPE_CHECKING, List, Dict, Tuple

from ..python_entities.positions import (
    Modifier as PythonModifier,
    Position as PythonPosition,
    ModifierGroup as PythonModifierGroup,
)

from .base import BaseIIKOService
from .serializers import (
    IIKONomenclatureSerializer,
    IIKOCategorySerializer,
    IIKOModifierGroupCreateSerializer,
)

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
    def _fetch_price_and_is_additional(position: Dict) -> Tuple[Decimal, bool]:
        try:
            size_price = position["sizePrices"].pop()["price"]
            return Decimal(size_price["currentPrice"]), bool(size_price["isIncludedInMenu"])
        except Exception as exc:
            print("Error while fetching position price:", exc)
            return Decimal(0), False

    @staticmethod
    def _fetch_modifier_groups(position) -> List[Dict]:
        modifier_groups = list()
        print("modifier groups:", modifier_groups)

        for modifier_group in position["groupModifiers"]:
            modifier_groups.append(PythonModifierGroup(
                outer_id=modifier_group["id"],
                min_amount=modifier_group["minAmount"],
                max_amount=modifier_group["maxAmount"],
                is_required=bool(modifier_group["required"]),
                modifiers=[  # noqa
                    PythonModifier(outer_id=modifier["id"],).__dict__
                    for modifier in modifier_group["childModifiers"]
                ],
            ).__dict__)

        return modifier_groups

    @staticmethod
    def sort_positions(positions):
        return sorted(
            positions,
            key=lambda x: bool(x.get('modifier_groups'))
        )

    def save_categories(self, categories: Dict) -> None:
        serializer = IIKOCategorySerializer(
            data=categories,
            many=True,
            context={
                "branch": self.instance,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def save_position_groups(self, position_groups):
        print("position groups:", position_groups)
        serializer = IIKOModifierGroupCreateSerializer(
            data=[
                position_group for position_group in position_groups
                if position_group.get("isGroupModifier")
            ],
            many=True,
            context={
                "local_brand_id": self.instance.local_brand_id,  # noqa
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def prepare_to_save(self, data: dict) -> List:
        positions: List[Dict] = list()
        categories = data.get("productCategories")
        position_groups = data.get("groups")

        if categories is not None:
            self.save_categories(categories)

        print("before save position groups")
        if position_groups is not None:
            self.save_position_groups(position_groups)
        print("after saving positions")

        for position in data.get("products", list()):
            price, is_additional = self._fetch_price_and_is_additional(position)

            positions.append(PythonPosition(
                price=price,
                outer_id=position.get('id'),
                is_additional=is_additional,
                iiko_name=position.get("name"),
                iiko_description=position.get("description"),
                category_outer_id=position.get("productCategoryId"),
                local_brand=self.instance.local_brand_id, # noqa
                modifier_groups=self._fetch_modifier_groups(position)  # noqa
            ).__dict__)

        return self.sort_positions(positions)

    def finalize_response(self, response):
        return response

    def save(self, prepared_data):
        serializer = self.save_serializer(
            data=self.prepare_to_save(prepared_data), many=True,
            context={"branch": self.instance}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()
