from django.contrib import admin

from apps.promotions.models import Promotion


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = [
        'slug',
        'image',
        'template',
        'type',
    ]
    prepopulated_fields = {"slug": ("template", 'type')}
