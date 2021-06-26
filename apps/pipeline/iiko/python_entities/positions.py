from uuid import UUID
from typing import List
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class Modifier:
    outer_id: UUID


@dataclass
class ModifierGroup:
    outer_id: UUID
    min_amount: int = 0
    max_amount: int = 0
    is_required: bool = False
    modifiers: List[Modifier] = None


@dataclass
class Position:
    iiko_name: str = None
    iiko_description: str = None
    category_outer_id: UUID = None
    outer_id: UUID = None
    price: Decimal = None
    local_brand: int = None
    is_additional: bool = False
    modifier_groups: List[ModifierGroup] = None
