from django.contrib import admin

# Register your models here.
from apps.payments.models import Payment, DebitCard

admin.site.register(Payment)
admin.site.register(DebitCard)
