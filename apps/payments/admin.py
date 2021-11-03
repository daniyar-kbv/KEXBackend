from django.contrib import admin

# Register your models here.
from apps.payments.models import Payment, DebitCard
from apps.common.admin import HistoryInline, ReadOnlyMixin


class PaymentAdmin(ReadOnlyMixin, admin.ModelAdmin):
    inlines = (HistoryInline,)


admin.site.register(Payment, PaymentAdmin)
admin.site.register(DebitCard)
