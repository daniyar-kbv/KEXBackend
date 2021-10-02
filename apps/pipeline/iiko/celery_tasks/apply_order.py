from requests.exceptions import ConnectionError, HTTPError, Timeout

from config import celery_app
from apps.orders import OrderStatuses
from apps.orders.models import Order

from ..integrations.apply_order import ApplyDeliveryOrder


@celery_app.task(
    name='iiko.call_order_apply_task',
    autoretry_for=(ConnectionError, HTTPError, Timeout),
    default_retry_delay=3,
    retry_kwargs={'max_retries': 2},
)
def call_order_apply_task(order_pk: int):
    order = Order.objects.get(id=order_pk)

    ApplyDeliveryOrder(instance=order).run()

    order.refresh_from_db()

    if order.status != OrderStatuses.APPLIED:
        call_order_apply_task.retry()


@celery_app.task(
    name='iiko.call_verify_order_task',
)
def call_verify_order_task(order_pk: int):
    order = Order.objects.get(id=order_pk)

    return 'success'


"""
from apps.orders.models import Order
from apps.pipeline.iiko.celery_tasks.apply_order import call_order_apply_task
t = Order.objects.get()
call_order_apply_task.delay(order_pk=t.id)
"""