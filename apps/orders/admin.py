from django.contrib import admin

from apps.common.admin import HistoryInline

from .models import Lead, Cart
from .models.orders import RatedOrder, RateStar, RateSample, Order, CouponGroup, Coupon


class LeadAdmin(admin.ModelAdmin):
    inlines = (HistoryInline,)


admin.site.register(Lead, LeadAdmin)
admin.site.register(RateSample)
admin.site.register(Order)
admin.site.register(Cart)


@admin.register(RateStar)
class RateStarAdmin(admin.ModelAdmin):
    filter_horizontal = ['rate_samples']


@admin.register(RatedOrder)
class RatedOrderAdmin(admin.ModelAdmin):
    filter_horizontal = ['rate_samples']


@admin.register(CouponGroup)
class CouponGroupAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        'group',
        'promocode',
        'start_date',
        'end_date'
    ]
    list_filter = ['group']
    search_fields = ['promocode']
    fields = [
        'group',
        'promocode',
        'description',
        'start_date',
        'end_date'
    ]