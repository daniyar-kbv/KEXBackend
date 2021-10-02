from django.contrib import admin

from apps.common.admin import HistoryInline, ReadOnlyMixin

from .models import Lead, Cart, Order, OrderStatusTransition


class OrderStatusTransitionInline(ReadOnlyMixin, admin.TabularInline):
    model = OrderStatusTransition
    extra = 0
    classes = ('collapse',)
    fields = ('status', 'status_reason', 'created_at')
    readonly_fields = ('status', 'status_reason', 'created_at')


class LeadAdmin(admin.ModelAdmin):
    inlines = (HistoryInline,)


class OrderAdmin(ReadOnlyMixin, admin.ModelAdmin):
    inlines = (HistoryInline, OrderStatusTransitionInline)


admin.site.register(Lead, LeadAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
