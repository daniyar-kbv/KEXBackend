from dataclasses import dataclass


@dataclass
class PaymentResponse:
    reason_code: int = None
    outer_id: str = None
    rrn: str = None
    status: str = None
    card_masked_number: str = None
    card_expiration_date: str = None
    card_type: str = None
    success: bool = False
