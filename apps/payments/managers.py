from django.db.models import QuerySet
from django.db.models.manager import BaseManager

from . import PaymentStatusTypes


class DebitCardsQuerySet(QuerySet):
    def active(self):
        return self.filter(card_token__isnull=False)

    def delete(self):
        return super().delete()


class DebitCardsManager(BaseManager.from_queryset(DebitCardsQuerySet)):
    ...


class PaymentsQueryset(QuerySet):
    def completed(self):
        return self.filter(status=PaymentStatusTypes.COMPLETED)

    def in_progress(self):
        return self.filter(status=PaymentStatusTypes.IN_PROGRESS)


class PaymentsManager(BaseManager.from_queryset(PaymentsQueryset)):
    ...
