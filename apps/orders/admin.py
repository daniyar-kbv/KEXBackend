from django.contrib import admin

from apps.common.admin import HistoryInline

from .models import Lead
from .models.orders import RatedOrder, RateStar, RateSample, Order


class LeadAdmin(admin.ModelAdmin):
    inlines = (HistoryInline,)


admin.site.register(Lead, LeadAdmin)
admin.site.register(RateSample)
admin.site.register(Order)


@admin.register(RateStar)
class RateStarAdmin(admin.ModelAdmin):
    filter_horizontal = ['rate_samples']


@admin.register(RatedOrder)
class RatedOrderAdmin(admin.ModelAdmin):
    filter_horizontal = ['rate_samples']
