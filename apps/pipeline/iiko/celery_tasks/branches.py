from config import celery_app

from apps.orders.models import Lead
from apps.pipeline.iiko.integrations.branches import FindOrganization


@celery_app.task(name="iiko.find_lead_organization")  # noqa
def find_lead_organization(
        lead_pk: int, change_type: str = None
) -> None:
    lead = Lead.objects\
        .select_related('address')\
        .prefetch_related('local_brand__branches')\
        .get(pk=lead_pk)

    return FindOrganization(
        instance=lead,
        change_type=change_type,
    ).run()
