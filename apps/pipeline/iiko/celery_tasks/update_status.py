from requests.exceptions import ConnectionError, HTTPError, Timeout

from config import celery_app
from apps.orders import OrderStatuses
from apps.orders.models import Order

from ..integrations.update_iiko_status import UpdateOrderStatus


@celery_app.task(
    name='iiko.update_order_status',
    queue='celery-gevent',
    autoretry_for=(ConnectionError, HTTPError, Timeout),
    default_retry_delay=60,
    max_retries=150,
    retry_kwargs={'max_retries': 100},
)
def update_order_status(order_pk: int):
    order = Order.objects.get(id=order_pk)

    if order.status in [OrderStatuses.DONE, OrderStatuses.CANCELLED]:
        return

    UpdateOrderStatus(order).run()
    order.refresh_from_db()


    update_order_status.retry()
