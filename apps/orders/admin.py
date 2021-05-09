from django.contrib import admin

from apps.common.admin import HistoryInline

from .models import Lead


class LeadAdmin(admin.ModelAdmin):
    inlines = (HistoryInline,)


admin.site.register(Lead, LeadAdmin)
