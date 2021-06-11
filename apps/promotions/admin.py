from django.contrib import admin

from apps.promotions.models import Promotion


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'type',
        'image',
        'priority',
        # 'slug',
    ]
    list_editable = ['priority']
    prepopulated_fields = {"slug": ("template", 'type')}
