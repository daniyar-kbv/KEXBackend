from django.contrib import admin

from apps.common.admin import HistoryInline, AbstractTitleModelForm, AbstractDescriptionModelForm, AbstractNameModelForm

from .models import Lead, Cart
from .models.orders import Order


class LeadAdmin(admin.ModelAdmin):
    inlines = (HistoryInline,)


admin.site.register(Lead, LeadAdmin)
admin.site.register(Order)
admin.site.register(Cart)
