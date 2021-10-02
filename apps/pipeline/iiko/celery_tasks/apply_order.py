from celery import Task
from requests.exceptions import ConnectionError, HTTPError, Timeout

from config import celery_app
from apps.orders import OrderStatuses
from apps.orders.models import Order

from ..integrations.apply_order import ApplyDeliveryOrder, VerifyDeliveryOrder


class OrderApplyTask(Task):
    name = 'iiko.order_apply_task'
    autoretry_for = (ConnectionError, HTTPError, Timeout)
    default_retry_delay = 5
    max_retries = 10

    @staticmethod
    def get_instance(order_pk) -> Order:
        return Order.objects.get(id=order_pk)

    def run(self, order_pk, *args, **kwargs):
        instance = self.get_instance(order_pk)

        ApplyDeliveryOrder(instance=instance).run()
        VerifyDeliveryOrder(instance=instance).run()

        instance.refresh_from_db()

        if instance.status == OrderStatuses.APPLIED:
            return

        self.retry()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        instance = self.get_instance(kwargs.get('order_pk'))
        instance.mark_as_apply_error()


order_apply_task = celery_app.register_task(OrderApplyTask())

"""
from apps.orders.models import Order
from apps.pipeline.iiko.celery_tasks.apply_order import order_apply_task
t = Order.objects.get()
order_apply_task.delay(order_pk=t.id)
"""