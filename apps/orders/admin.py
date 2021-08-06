from django.contrib import admin

from apps.common.admin import HistoryInline, AbstractTitleModelForm, AbstractDescriptionModelForm, AbstractNameModelForm

from .models import Lead, Cart
from .models.orders import RatedOrder, RateStar, RateSample, Order, CouponGroup, Coupon


class LeadAdmin(admin.ModelAdmin):
    inlines = (HistoryInline,)


admin.site.register(Lead, LeadAdmin)
admin.site.register(Order)
admin.site.register(Cart)


class RateStarForm(AbstractTitleModelForm, AbstractDescriptionModelForm):
    class Meta:
        model = RateStar
        exclude = ('title', 'description')


@admin.register(RateStar)
class RateStarAdmin(admin.ModelAdmin):
    filter_horizontal = ['rate_samples']
    form = RateStarForm


@admin.register(RatedOrder)
class RatedOrderAdmin(admin.ModelAdmin):
    filter_horizontal = ['rate_samples']


class RateSampleForm(AbstractNameModelForm):
    class Meta:
        model = RateSample
        exclude = ('name',)


@admin.register(RateSample)
class RateSampleAdmin(admin.ModelAdmin):
    list_display = ['name']
    form = RateSampleForm


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