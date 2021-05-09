from config import celery_app

from apps.orders.models import Lead
from apps.pipeline.iiko.integrations.organizations import FindOrganization


@celery_app.task(name="iiko.find_lead_organization")  # noqa
def find_lead_organization(lead_pk: int):
    lead = Lead.objects.get(pk=lead_pk)

    return FindOrganization(instance=lead).run()
