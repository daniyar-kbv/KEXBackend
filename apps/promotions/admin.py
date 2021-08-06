from django.contrib import admin

from apps.common.admin import AbstractNameModelForm, AbstractTemplateModelForm, AbstractDescriptionModelForm, \
    AbstractImageModelForm
from apps.notifications.admin import InlineNotification
from apps.promotions.models import Promotion, Participation


class PromotionForm(
    AbstractNameModelForm,
    AbstractTemplateModelForm,
    AbstractDescriptionModelForm,
    AbstractImageModelForm
):
    class Meta:
        model = Promotion
        exclude = ('name', 'description', 'image')


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
    filter_horizontal = ['local_brand']
    form = PromotionForm


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = [
        # 'user',
        'instagram_username',
        # 'promotion'
    ]