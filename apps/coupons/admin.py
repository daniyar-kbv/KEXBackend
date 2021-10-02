from django.contrib import admin

from .models import Coupon, CouponGroup


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
