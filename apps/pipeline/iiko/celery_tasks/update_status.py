from requests.exceptions import ConnectionError, HTTPError, Timeout

from config import celery_app
from apps.orders import OrderStatuses
from apps.orders.models import Order

from ..integrations.update_iiko_status import UpdateOrderStatus


@celery_app.task(
    name='iiko.update_order_status',
    autoretry_for=(ConnectionError, HTTPError, Timeout),
    default_retry_delay=60,
    retry_kwargs={'max_retries': 100},
)
def update_order_status(order_pk: int):
    order = Order.objects.get(id=order_pk)
    UpdateOrderStatus(order).run()
    order.refresh_from_db()

    if order.status in [OrderStatuses.DONE, OrderStatuses.CANCELLED]:
        return

    update_order_status.retry()
