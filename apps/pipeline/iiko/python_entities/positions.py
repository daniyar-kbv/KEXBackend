from uuid import UUID
from typing import List
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class Modifier:
    outer_id: UUID
    min_amount: int = 1
    max_amount: int = 1
    required: bool = False


@dataclass
class SizePrice:
    price: Decimal = Decimal(0)
    outer_id: UUID = None


@dataclass
class Position:
    outer_id: UUID = None

    local_brand: int = None
    iiko_name: str = None
    iiko_description: str = None

    size_prices: List[SizePrice] = None
    modifiers: List[Modifier] = None
