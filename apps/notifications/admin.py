from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline

from . import PushTypes
from .models import Notification, FirebaseToken, NotificationTemplate
from apps.common.admin import AbstractTitleModelForm, AbstractDescriptionModelForm
from ..orders.models import Order
from ..promotions.models import Promotion


class InlineNotification(GenericStackedInline):
    verbose_name = "Пуш уведомление для акции"
    model = Notification
    min_num = 1
    max_num = 1
    fields = (
        'title',
        'description'
    )
    # ct_fk_field = "config_object_id"
    # ct_field = "config_content_type"


class NotificationForm(AbstractTitleModelForm, AbstractDescriptionModelForm):
    ref_object = forms.IntegerField(label="Связанный объект", required=False)

    class Meta:
        fields = (
            'title_ru',
            'title_kk',
            'title_en',
            'description_ru',
            'description_kk',
            'description_en',
            'uuid',
            'date',
            'push_type',
            'ref_object'
        )

    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
        ref_object = self.instance.content_object if self.instance else None
        queryset = ref_object._meta.model.objects.all() if ref_object else None
        initial = ref_object.id if ref_object else None
        self.fields['ref_object'] = forms.ModelChoiceField(
            label="Связанный объект",
            required=False,
            queryset=queryset or Promotion.objects.all(),
            initial=initial
        )

    def save(self, commit=True):
        obj = super(NotificationForm, self).save(commit=False)

        ref_oid = self.cleaned_data['ref_object']
        print('ref_oid in save: ', ref_oid)
        if ref_oid:
            ref_oid = ref_oid.id
            if obj.push_type == PushTypes.PROMOTION:
                obj.content_object = Promotion.objects.get(id=ref_oid)
            elif obj.push_type == PushTypes.ORDER_STATUS_UPDATE or obj.push_type == PushTypes.ORDER_RATE:
                obj.content_object = Order.objects.get(id=ref_oid)

        if commit:
            obj.save()
        return obj


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'title', 'push_type', 'date']
    readonly_fields = ['uuid']
    form = NotificationForm
    # fields = (
    #     'uuid',
    #     'title',
    #     'description',
    #     'push_type',
    #     'date',
    # )


class NotificationTemplateForm(AbstractTitleModelForm, AbstractDescriptionModelForm):
    class Meta:
        model = NotificationTemplate
        fields = (
            'push_type',
            'title_ru',
            'title_kk',
            'title_en',
            'description_ru',
            'description_kk',
            'description_en',
        )


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = [
        'push_type',
        'title',
        'description'
    ]
    form = NotificationTemplateForm


@admin.register(FirebaseToken)
class FirebaseTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'fbtoken']
    readonly_fields = ['token']
    fields = (
        'token',
        'user'
    )

    def fbtoken(self, obj):
        if obj.token:
            return f"{obj.token[:50]}..."
