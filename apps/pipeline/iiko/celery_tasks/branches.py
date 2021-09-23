from config import celery_app
from django.core.cache import cache

from apps.orders.models import Lead
from apps.pipeline.iiko.integrations.branches import FindOrganization
from apps.partners.exceptions import TerminalNotFound


@celery_app.task(name="iiko.find_lead_organization")  # noqa
def find_lead_organization(lead_pk: int):
    lead = Lead.objects.get(pk=lead_pk)

    found = FindOrganization(instance=lead).run()

    lead.refresh_from_db()

    if (not found or
        lead.branch is None or
        not lead.cart.positions.exists()
    ):
        if lead.user and lead.user.addresses.filter(address_id=lead.address_id).exists():
            lead.user.addresses.filter(address_id=lead.address_id).delete()
        lead.address.delete()

        raise TerminalNotFound

    """
    add branch to cache 
    for frequent updating of "stop list"
    p.s. expires in 1 hour
    """
    cache.set(str(lead.branch.outer_id), True, 60 * 60)
