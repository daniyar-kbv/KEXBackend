from django.contrib import admin

from .models import Notification, FirebaseToken


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
