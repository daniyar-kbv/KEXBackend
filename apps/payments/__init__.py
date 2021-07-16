from django.db.models import TextChoices


class CurrencyTypes(TextChoices):
    KZT = "KZT", "Казахстанское тенге (KZT)"


class PaymentTypes(TextChoices):
    DEBIT_CARD = "DEBIT_CARD", "Оплата дебетовой картой"
    GOOGLE_PAY = "GOOGLE_PAY", "Оплата через GooglePay"
    APPLE_PAY = "APPLE_PAY", "Оплата через ApplePay"


class PaymentStatusTypes(TextChoices):
    NEW = "NEW", "Новый"
    COMPLETED = 'COMPLETED', "Завершено"
    CANCELLED = 'CANCELLED', "Отменено"
    DECLINED = 'DECLINED', "Отказано"
    AWAITING_AUTHENTICATION = "AWAITING_AUTHENTICATION", "Ожидается 3ds авторизация"
