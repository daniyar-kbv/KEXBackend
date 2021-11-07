from django.contrib import admin
from django.core.exceptions import ValidationError

from apps.common.admin import HistoryInline, ReadOnlyMixin
from apps.payments.models import Payment

from . import OrderStatuses
from .models import Lead, Cart, Order, OrderStatusTransition


class PaymentsInline(ReadOnlyMixin, admin.TabularInline):
    model = Payment
    extra = 0
    classes = ('collapse',)


class OrderStatusTransitionInline(ReadOnlyMixin, admin.TabularInline):
    model = OrderStatusTransition
    extra = 0
    classes = ('collapse',)
    fields = ('status', 'status_reason', 'created_at')
    readonly_fields = ('status', 'status_reason', 'created_at')


class LeadAdmin(admin.ModelAdmin):
    inlines = (HistoryInline,)


class OrderAdmin(ReadOnlyMixin, admin.ModelAdmin):
    inlines = (HistoryInline, OrderStatusTransitionInline, PaymentsInline)
    actions = 'retry_apply_to_iiko', 'cancel_order'

    def cancel_order(self, request, queryset):
        from apps.pipeline.iiko.integrations.cancel_order import CancelDeliveryOrder
        from django.contrib import messages

        if queryset.count() != 1:
            self.message_user(request, 'Можно отменять по одному заказу', messages.ERROR)
            return

        order = queryset.first()
        cancel_result = CancelDeliveryOrder(order).run()
        if not cancel_result:
            self.message_user(request, 'Ошибка при отмене заказа', messages.ERROR)
            return

        self.message_user(request, 'Успешно оформлен возврат', messages.SUCCESS)
        print('cancel_result', cancel_result)

    cancel_order.short_description = 'Отмена заказа'


    def retry_apply_to_iiko(self, request, queryset):
        from apps.pipeline.iiko.celery_tasks import order_apply_task

        for el in queryset:
            if el.status == OrderStatuses.APPLY_ERROR:
                order_apply_task.delay(order_pk=el.pk)

    retry_apply_to_iiko.short_description = "Повторная выгрузка в IIKO"


admin.site.register(Lead, LeadAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
