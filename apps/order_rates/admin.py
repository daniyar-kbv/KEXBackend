from django.contrib import admin

# Register your models here.
from apps.common.admin import AbstractTitleModelForm, AbstractNameModelForm, AbstractDescriptionModelForm
from .models import RateStar, RatedOrder, RateSample


class RateStarForm(AbstractTitleModelForm, AbstractDescriptionModelForm):
    class Meta:
        model = RateStar
        exclude = ('title', 'description')


@admin.register(RateStar)
class RateStarAdmin(admin.ModelAdmin):
    filter_horizontal = ['rate_samples']
    form = RateStarForm


@admin.register(RatedOrder)
class RatedOrderAdmin(admin.ModelAdmin):
    filter_horizontal = ['rate_samples']


class RateSampleForm(AbstractNameModelForm):
    class Meta:
        model = RateSample
        exclude = ('name',)


@admin.register(RateSample)
class RateSampleAdmin(admin.ModelAdmin):
    list_display = ['name']
    form = RateSampleForm
