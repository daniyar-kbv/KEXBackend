from django.db.models import QuerySet
from django.db.models.manager import BaseManager

from . import PaymentStatusTypes


class PaymentsQueryset(QuerySet):
    def completed(self):
        return self.filter(status=PaymentStatusTypes.COMPLETED)


class PaymentsManager(BaseManager.from_queryset(PaymentsQueryset)):
    ...
