from django.shortcuts import get_object_or_404

from apps.orders.models import Lead

from .exceptions import BranchIsClosed


def check_branch_is_open_and_active(function):
    def _function(request, *args, **kwargs):
        print('DECORATOR (check_branch_is_open) is called')
        lead: Lead = get_object_or_404(
            Lead.objects.select_related('branch', 'local_brand'),
            uuid=kwargs.get('lead_uuid') or request.data.get('lead')
        )

        if not lead.branch.is_active or not lead.local_brand.is_active or \
                not lead.branch.delivery_times.open().exists():
            print('DECORATOR (check_branch_is_open) raised BranchIsCalled')
            lead.drop_delivery()
            raise BranchIsClosed

        return function(request, *args, **kwargs)

    return _function


def update_delivery_positions(function):
    def _function(request, *args, **kwargs):
        print('DECORATOR (update_delivery_positions) is called')
        lead: Lead = get_object_or_404(
            Lead.objects.select_related('branch'),
            uuid=kwargs['lead_uuid']
        )

        lead.update_delivery_params()

        return function(request, *args, **kwargs)

    return _function
