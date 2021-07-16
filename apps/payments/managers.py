from django.db.models import QuerySet
from django.db.models.manager import BaseManager

from . import PaymentStatusTypes


class DebitCardsQuerySet(QuerySet):
    def is_active(self):
        return self.filter(is_active=True)


class DebitCardsManager(BaseManager.from_queryset(DebitCardsQuerySet)):
    ...


class PaymentsQueryset(QuerySet):
    def completed(self):
        return self.filter(status=PaymentStatusTypes.COMPLETED)


class PaymentsManager(BaseManager.from_queryset(PaymentsQueryset)):
    ...
