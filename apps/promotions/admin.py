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
        # fields = (
        #     'name_ru', 'name_kk', 'name_en',
        #     'description_ru', 'description_kk', 'description_en',
        #     'image_ru', 'image_kk', 'image_en',
        #     'template_ru', 'template_kk', 'template_en',
        #     'priority',
        #     'web_url',
        #     'slug',
        #     'promo_type',
        #     'local_brand',
        #     'start_date',
        #     'end_date'
        # )


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'promo_type',
        'image',
        'priority',
        # 'web_url',
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