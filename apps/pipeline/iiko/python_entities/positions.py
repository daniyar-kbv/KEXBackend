from uuid import UUID
from typing import List
from decimal import Decimal
from dataclasses import dataclass


@dataclass
class Modifier:
    outer_id: UUID
    min_amount: int = None
    max_amount: int = None
    required: bool = False


@dataclass
class Position:
    outer_id: UUID = None

    iiko_brand: int = None
    iiko_name: str = None
    iiko_description: str = None

    price: Decimal = None
    modifiers: List[Modifier] = None
