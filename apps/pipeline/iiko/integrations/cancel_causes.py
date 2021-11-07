from typing import Any

from .base import BaseIIKOService
from .serializers import IIKOCancelCauseSerializer


class GetPayments(BaseIIKOService):
    """Получение причины отказа"""
    endpoint = 'api/1/cancel_causes'
    save_serializer = IIKOCancelCauseSerializer

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
            'uuid': cancel_cause.get('id'),
            'name': cancel_cause.get('name'),
        } for cancel_cause in data.get('cancelCauses')
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
