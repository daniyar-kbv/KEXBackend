from django.contrib import admin

from apps.notifications.admin import InlineNotification
from apps.promotions.models import Promotion, Participation


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'promo_type',
        'image',
        'priority',
        # 'slug',
    ]
    list_editable = ['priority']
    prepopulated_fields = {"slug": ("template", 'promo_type')}
    inlines = [InlineNotification]


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = [
        # 'user',
        'instagram_username',
        # 'promotion'
    ]