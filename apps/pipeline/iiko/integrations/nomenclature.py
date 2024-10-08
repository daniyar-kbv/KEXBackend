from decimal import Decimal
from typing import TYPE_CHECKING, List, Dict, Tuple

from apps.nomenclature.models import PositionTypes

from .base import BaseIIKOService
from .serializers import (
    IIKONomenclatureSerializer,
    IIKOCategorySerializer,
    IIKOModifierGroupCreateSerializer,
)

if TYPE_CHECKING:
    from apps.partners.models import LocalBrand, Branch
    from apps.nomenclature.models import BranchPosition


class GetLocalBrandNomenclature(BaseIIKOService):
    """Получение меню организации"""
    endpoint = "/api/1/nomenclature"
    instance: 'LocalBrand' = None
    save_serializer = IIKONomenclatureSerializer

    position_types = {
        "Dish": PositionTypes.MAIN,
        "Modifier": PositionTypes.MODIFIER,
    }

    def get_first_active_organization_outer_id(self):
        random_branch = self.instance.branches.active().first()

        if random_branch is not None:
            return str(random_branch.outer_id)

    def run_service(self):
        return self.fetch(json={
            "organizationId": self.get_first_active_organization_outer_id()
        })

    @staticmethod
    def _fetch_modifier_groups(position) -> List[Dict]:
        return [
            {
                "outer_id": modifier_group["id"],
                "min_amount": modifier_group["minAmount"],
                "max_amount": modifier_group["maxAmount"],
                "is_required": bool(modifier_group["required"]),
                "modifiers": [
                    {"outer_id": modifier["id"]}
                    for modifier in modifier_group["childModifiers"]
                ],
            } for modifier_group in position.get("groupModifiers", list())
        ]

    def sort_positions(self, positions):  # noqa
        return sorted(
            positions,
            key=lambda x: bool(x.get('modifier_groups'))
        )

    def save_categories(self, categories: Dict) -> None:
        serializer = IIKOCategorySerializer(
            data=categories,
            many=True,
            context={
                "local_brand": self.instance,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

    @staticmethod
    def fetch_modifier_groups(position_groups):
        return [
            position_group for position_group in position_groups
            if position_group.get("isGroupModifier")
        ]

    def save_modifier_groups(self, modifier_groups):
        serializer = IIKOModifierGroupCreateSerializer(
            data=modifier_groups,
            many=True,
            context={
                "local_brand": self.instance
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def filter_products(self, products):  # noqa
        if not products:
            return list()

        return list(filter(
            lambda x: (
                x['productCategoryId'] or x.get("type") == "Modifier"
            ), products)
        )

    def prepare_to_save(self, data: dict) -> List:
        positions: List[Dict] = list()
        categories = data.get("productCategories")
        position_groups = data.get("groups")

        if categories is not None:
            self.save_categories(categories)

        if position_groups is not None:
            self.save_modifier_groups(
                self.fetch_modifier_groups(position_groups)
            )

        products = self.filter_products(data.get("products"))

        for position in products:
            positions.append({
                "outer_id": position.get('id'),
                "position_type": self.position_types.get(position.get("type")),
                "iiko_name": position.get("name"),
                "iiko_description": position.get("description"),
                "category_outer_id": position.get("productCategoryId"),
                "modifier_groups": self._fetch_modifier_groups(position),
                "local_brand": self.instance.pk,
            })

        return self.sort_positions(positions)

    def finalize_response(self, response):
        return response

    def save(self, prepared_data):
        serializer = self.save_serializer(
            data=self.prepare_to_save(prepared_data), many=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()


class GetBranchNomenclaturePrices(BaseIIKOService):
    """Получение цены меню"""
    endpoint = "/api/1/nomenclature"
    instance: 'Branch' = None

    def get_local_brand_pk(self):  # noqa
        return self.instance.local_brand_id

    def run_service(self):
        return self.fetch(json={
            "organizationId": str(self.instance.outer_id)
        })

    @staticmethod
    def fetch_price(position: Dict) -> Decimal:
        try:
            size_price = position["sizePrices"][0]["price"]
            return Decimal(size_price["currentPrice"])
        except Exception as exc:
            print("Error while fetching position price:", exc)
            return Decimal(0)

    def filter_products(self, products):  # noqa
        if not products:
            return []

        return list(filter(
            lambda x: (
                x['productCategoryId'] or x.get("type") == "Modifier"
            ), products)
        )

    def set_false_branch_positions_existing_flag(self):
        self.instance.branch_positions.all().update(is_exists=False)

    def set_false_branch_modifier_groups_existsing_flag(self):
        self.instance.branch_modifier_groups.all().update(is_exists=False)

    @staticmethod
    def fetch_modifier_groups(position_groups):
        return [
            position_group for position_group in position_groups
            if position_group.get("isGroupModifier")
        ]

    def fetch_branch_modifier_groups(self, modifier_groups: List):
        self.instance.branch_modifier_groups.filter(
            modifier_group__outer_id__in=[i['id'] for i in modifier_groups]
        ).update(is_exists=True)

    def fetch_branch_position_prices(self, products: List):
        for product in products:
            if self.instance.branch_positions.filter(position__outer_id=product.get('id')).exists():
                branch_position: 'BranchPosition' = self.instance.branch_positions.get(
                    position__outer_id=product.get('id')
                )
                branch_position.is_exists = True
                branch_position.price = self.fetch_price(product)
                branch_position.save(update_fields=['is_exists', 'price'])

    def prepare_to_save(self, data: dict):
        self.set_false_branch_modifier_groups_existsing_flag()
        self.fetch_branch_modifier_groups(self.fetch_modifier_groups(data.get("groups")))
        self.set_false_branch_positions_existing_flag()
        self.fetch_branch_position_prices(self.filter_products(data.get('products')))

    def finalize_response(self, response):
        ...

    def save(self, prepared_data):
        self.prepare_to_save(prepared_data)
