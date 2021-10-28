from django.shortcuts import get_object_or_404

from apps.orders.models import Lead

from .exceptions import BranchIsClosedError, OutOfStockError


def check_branch_is_open_and_active(function):
    def _function(request, *args, **kwargs):
        print('DECORATOR (check_branch_is_open_and_active) is called')
        lead: Lead = get_object_or_404(
            Lead.objects.select_related('branch', 'local_brand'),
            uuid=kwargs.get('lead_uuid') or request.data.get('lead')
        )

        if not lead.branch.is_active or not lead.local_brand.is_active or \
                not lead.branch.delivery_times.open().exists():
            print('DECORATOR (check_branch_is_open) raised BranchIsCalled')
            lead.drop_delivery()
            raise BranchIsClosedError

        return function(request, *args, **kwargs)

    return _function


def check_out_of_stock(function):
    def _function(request, *args, **kwargs):
        print('DECORATOR (check_positions_is_active) is called')
        lead: Lead = get_object_or_404(
            Lead.objects.select_related('cart'),
            uuid=kwargs.get('lead_uuid') or request.data.get('lead')
        )

        if lead.cart.has_unavailable_positions:
            print('DECORATOR (check_out_of_stock) raised OutOfStockError')
            raise OutOfStockError

        return function(request, *args, **kwargs)

    return _function


def update_delivery_positions(function):
    def _function(request, *args, **kwargs):
        print('DECORATOR (update_delivery_positions) is called')
        lead: Lead = get_object_or_404(
            Lead.objects.select_related('branch'),
            uuid=kwargs['lead_uuid'] or request.data.get('lead')
        )

        lead.update_delivery_params()

        return function(request, *args, **kwargs)

    return _function
