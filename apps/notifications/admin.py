from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline

from .models import Notification, FirebaseToken, NotificationTemplate
from apps.common.admin import AbstractTitleModelForm, AbstractDescriptionModelForm


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


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'title', 'push_type', 'date']
    readonly_fields = ['uuid']
    fields = (
        'uuid',
        'title',
        'description',
        'push_type',
        'date',
    )


class NotificationTemplateForm(AbstractTitleModelForm, AbstractDescriptionModelForm):
    class Meta:
        model = NotificationTemplate
        fields = '__all__'


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = [
        # 'name',
        'title',
        'description'
    ]
    fields = (
        # 'name',
        'title',
        'description'
    )
    form = NotificationTemplateForm


@admin.register(FirebaseToken)
class FirebaseTokenAdmin(admin.ModelAdmin):
    list_display = ['lead_uuid', 'user', 'fbtoken']
    readonly_fields = ['token']
    fields = (
        'lead',
        'token',
        'user'
    )

    def lead_uuid(self, obj):
        return obj.lead.uuid

    def fbtoken(self, obj):
        if obj.token:
            return f"{obj.token[:50]}..."
