from config import celery_app
from django.core.cache import cache

from apps.orders.models import Lead
from apps.pipeline.iiko.integrations.organizations import FindOrganization
from apps.partners.exceptions import TerminalNotFound


@celery_app.task(name="iiko.find_lead_organization")  # noqa
def find_lead_organization(lead_pk: int):
    lead = Lead.objects.get(pk=lead_pk)

    found = FindOrganization(instance=lead).run()

    if not found:
        raise TerminalNotFound

    lead.refresh_from_db()

    """
    adding an branch to cache 
    for frequent updating of "stop list"
    p.s. expires in 2 hours
    """
    cache.set(str(lead.branch.outer_id), True, 2 * 60 * 60)
