from django.contrib import admin

from apps.notifications.admin import InlineNotification
from apps.promotions.models import Promotion, Participation
from apps.common.admin import (
    AbstractNameModelForm,
    AbstractTemplateModelForm,
    AbstractDescriptionModelForm,
    MultiLanguageImageModelInline,
)


class PromotionForm(
    AbstractNameModelForm,
    AbstractTemplateModelForm,
    AbstractDescriptionModelForm,
):
    class Meta:
        model = Promotion
        exclude = ('name', 'description')


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'promo_type',
        'priority',
    ]
    list_editable = ['priority']
    prepopulated_fields = {"slug": ("template", 'promo_type')}
    inlines = [
        InlineNotification, MultiLanguageImageModelInline
    ]
    filter_horizontal = ['local_brand']
    form = PromotionForm


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = 'instagram_username',
