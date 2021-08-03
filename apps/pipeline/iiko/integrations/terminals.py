from typing import Any

from apps.partners.models import Branch

from .base import BaseIIKOService


class GetLocalBrandTerminals(BaseIIKOService):
    """Получение терминалов организации Бренда"""
    endpoint = 'api/1/terminal_groups'

    def get_branches_list(self):
        return list(
            str(i) for i in self.instance.branches.values_list('outer_id', flat=True)  # noqa
        )

    def run_service(self) -> Any:
        return self.fetch(json={
            'organizationIds': self.get_branches_list(),
            'includeDisabled': False,
        })

    def filter_terminals(self, terminals):
        return list(filter(
            lambda x: (
                    isinstance(x.get('items'), list) and
                    len(x.get("items")) >= 1
            ), terminals)
        )

    def prepare_to_save(self, data):
        filtered_terminals = self.filter_terminals(
            data.get("terminalGroups", [])
        )
        return [{
            "branch_outer_id": terminal["organizationId"],
            "terminal_id": terminal['items'][0]["id"],
        } for terminal in filtered_terminals
        ]

    def save(self, prepared_data):
        for i in self.prepare_to_save(prepared_data):
            branch = Branch.objects.get(outer_id=i["branch_outer_id"])
            branch.terminal_id = i["terminal_id"]
            branch.save(update_fields=["terminal_id"])


class CheckLocalBrandOrganizationsLiveness(BaseIIKOService):
    """Проверка активности терминалов организации бренда"""
    endpoint = "api/1/terminal_groups/is_alive"

    def get_branches_list(self):
        return list(
            str(i) for i in self.instance.branches.active().values_list('outer_id', flat=True)  # noqa
        )

    def get_terminals_list(self):
        return list(
            str(i) for i in self.instance.branches.active().values_list("terminal_id", flat=True)  # noqa
        )

    def run_service(self) -> Any:
        return self.fetch(json={
            'organizationIds': self.get_branches_list(),
            'terminalGroupIds': self.get_terminals_list(),
        })

    def prepare_to_save(self, data):
        return list(filter(
            lambda x: (
                'isAlive' in x,
                Branch.objects.filter(
                    terminal_id=x.get("terminalGroupId"),
                    outer_id=x.get("organizationId"),
                ).exists()
            ), data.get("isAliveStatus", []))
        )

    def save(self, prepared_data):
        prepared_data = self.prepare_to_save(prepared_data)
        for i in prepared_data:
            branch = Branch.objects.get(outer_id=i["organizationId"])
            branch.is_alive = i["isAlive"]
            branch.save(update_fields=["is_alive"])
