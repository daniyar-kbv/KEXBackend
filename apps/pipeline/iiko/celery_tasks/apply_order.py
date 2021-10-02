from requests.exceptions import ConnectionError, HTTPError, Timeout

from config import celery_app
from apps.orders.models import Order

from ..integrations.apply_order import ApplyDeliveryOrder


@celery_app.task(
    name='iiko.call_order_apply_task',
    autoretry_for=(ConnectionError, HTTPError, Timeout),
    default_retry_delay=10,
    retry_kwargs={'max_retries': 20},
)
def call_order_apply_task(order_pk: int):
    order = Order.objects.get(id=order_pk)

    return ApplyDeliveryOrder(
        instance=order
    ).run()


@celery_app.task(
    name='iiko.call_verify_order_task',
)
def call_verify_order_task(order_pk: int):
    order = Order.objects.get(id=order_pk)

    return 'success'
