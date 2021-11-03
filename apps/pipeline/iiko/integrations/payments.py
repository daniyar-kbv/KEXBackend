from typing import Any

from .base import BaseIIKOService
from .serializers import IIKOPaymentTypeSerializer


class GetPayments(BaseIIKOService):
    """Получение типов платежей системы"""
    endpoint = 'api/1/payment_types'
    save_serializer = IIKOPaymentTypeSerializer

    def get_first_active_organization_outer_id(self):
        random_branch = self.instance.branches.active().first()

        if random_branch is not None:
            return str(random_branch.outer_id)

    def run_service(self) -> Any:
        return self.fetch(json={
            'organizationIds': [self.get_first_active_organization_outer_id()],
        })

    def prepare_to_save(self, data: dict):
        return [{
            'iiko_uuid': payment_type.get('id'),
            'code': payment_type.get('paymentTypeKind'),
            'name': payment_type.get('name')
        } for payment_type in data.get('paymentTypes', [])
        if payment_type.get('terminalGroups')
        ]

    def finalize_response(self, response):
        return response

    def save(self, prepared_data):
        prepared_data = self.prepare_to_save(prepared_data)

        if not prepared_data:
            return

        serializer = self.save_serializer(
            data=prepared_data,
            context={'local_brand': self.instance},
            many=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
