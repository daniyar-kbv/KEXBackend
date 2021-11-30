from datetime import time
from typing import Any

from apps.partners.models import Branch, BranchDeliveryTime

from .base import BaseIIKOService


class GetBranchZones(BaseIIKOService):
    """Получение данных зон организации"""
    endpoint = 'api/1/delivery_restrictions'

    def get_first_active_organization_outer_id(self):
        random_branch = self.instance.branches.active().first()

        if random_branch is not None:
            return str(random_branch.outer_id)

    def run_service(self) -> Any:
        return self.fetch(json={
            'organizationIds': [self.get_first_active_organization_outer_id()],
        })

    @staticmethod
    def int_to_time(int_time: int) -> time:
        if not isinstance(int_time, int):
            int_time = int(int_time)

        hours = int_time // 60
        minutes = int_time % 60

        return time(hours, minutes)

    def save(self, prepared_data):
        print('PreparedData is:', prepared_data)
        delivery_restrictions = prepared_data.get('deliveryRestrictions')

        if not delivery_restrictions:
            return

        for delivery_restriction in delivery_restrictions:
            try:
                branch = Branch.objects.get(outer_id=delivery_restriction['organizationId'])

                for restriction in delivery_restriction['restrictions']:
                    BranchDeliveryTime.objects.update_or_create(
                        branch=branch,
                        zone_name=restriction['zone'],
                        defaults={
                            'start_time': self.int_to_time(restriction['from']),
                            'end_time': self.int_to_time(restriction['to'])
                        }
                    )

            except Exception as exc:
                print(exc)
