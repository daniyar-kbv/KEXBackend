from django.shortcuts import get_object_or_404

from apps.orders.models import Lead

from .exceptions import BranchIsClosed


def check_branch_is_open(function):
    def _function(request, *args, **kwargs):
        lead = get_object_or_404(
            Lead.objects.select_related('branch'),
            uuid=kwargs['lead_uuid']
        )

        if not lead.branch.delivery_times.open().exists():
            raise BranchIsClosed

        return function(request, *args, **kwargs)

    return _function
