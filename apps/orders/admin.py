from django.contrib import admin

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
    list_filter = 'local_brand', 'branch', 'status'
    search_fields = 'user__mobile_phone',
    actions = 'retry_apply_to_iiko', 'cancel_order'
    list_display = ('lead', 'branch', 'local_brand', 'status', 'status_reason', 'user', 'outer_id')

    fieldsets = (
        ("Main", {
            "fields": (
                'lead',
                'user_info',
                'full_address',
                "branch",
                "local_brand",
                'outer_id',
                'status',
                'status_reason',
                'cart_info'
            )}),
    )

    def user_info(self, obj):
        if obj.user:
            return f"{obj.user.name}-{obj.user.mobile_phone}"

    def full_address(self, obj):
        if obj.lead and obj.lead.address:
            return obj.lead.address.full_address()

    def cart_info(self, obj):
        if obj.cart:
            s = ''
            for i_index, i in enumerate(obj.cart.positions.all()):
                s += f'{i_index+1}. {i.branch_position.name}(количество {i.count}, цена {i.branch_position.price})' + '\n'
                if i.modifiers.all().exists():
                    s += 'Модификаторы:'
                    for j_index, j in enumerate(i.modifiers.all()):
                        s += f'{j_index+1}. {j.branch_position.name}(количество {j.count}, цена {j.branch_position.price})' + '\n'
                s += '\n'

            return s

    def cancel_order(self, request, queryset):
        from apps.pipeline.iiko.integrations.cancel_order import CancelDeliveryOrder
        from apps.pipeline.cloudpayments.integrations.cancel_payment import CancelPayment
        from django.contrib import messages

        if queryset.count() != 1:
            self.message_user(request, 'Можно отменять по одному заказу', messages.ERROR)
            return

        order: Order = queryset.first()
        if not order.is_allowed_to_cancel:
            self.message_user(request, 'Статус не позволяет отменить заказ', messages.ERROR)
            return

        iiko_cancel_result = CancelDeliveryOrder(order).run()
        print('iiko cancel_result', iiko_cancel_result)

        if not iiko_cancel_result:
            self.message_user(request, 'Ошибка при отмене заказа', messages.ERROR)
            return

        cloudpayments_cancel_result = True

        if order.completed_payment:
            cloudpayments_cancel_result = CancelPayment(order.completed_payment).run()

        if not cloudpayments_cancel_result:
            self.message_user(request, 'Успешно оформлен возврат, ошибка в CloudPayments', messages.SUCCESS)
        else:
            self.message_user(request, 'Успешно оформлен возврат', messages.SUCCESS)

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
