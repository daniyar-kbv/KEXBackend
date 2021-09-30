from config import celery_app

from apps.orders.models import Order

from ..integrations.apply_order import ApplyDeliveryOrder


@celery_app.task(name='iiko.apply_delivery_order')
def apply_delivery_order(order_pk: int):
    order = Order.objects\
        .prefetch_related(
            "cart__position",
            "cart__position__modifiers",
        ).get(id=order_pk)

    return ApplyDeliveryOrder(
        instance=order
    ).run()
