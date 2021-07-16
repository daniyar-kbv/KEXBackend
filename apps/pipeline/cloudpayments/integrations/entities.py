from dataclasses import dataclass


@dataclass
class PaymentTransaction:
    success: bool = False
    reason_code: int = None
    outer_id: str = None
    rrn: str = None
    status: str = None


@dataclass
class DebitCard:
    card_masked_number: str = None
    card_expiration_date: str = None
    card_token: str = None
    card_type: str = None


@dataclass
class Authorization3DS:
    pa_req: str = None
    acs_url: str = None


@dataclass
class PaymentResponse:
    debit_card: DebitCard
    payment_transaction: PaymentTransaction
    authorization_3ds: Authorization3DS
