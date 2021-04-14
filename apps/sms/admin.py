from django.contrib import admin

from .models import OTP, SMSMessage, SMSTemplate


class SMSMessageAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "uuid",
        "recipients",
        "content",
        "error_code",
        "error_description",
    )
    list_display_links = (
        "created_at",
        "uuid",
    )
    readonly_fields = (
        "created_at",
        "uuid",
        "recipients",
        "content",
        "error_code",
        "error_description",
    )
    ordering = ("-created_at",)


class OTPAdmin(admin.ModelAdmin):
    list_display = ("created_at", "mobile_phone", "verified", "code")
    list_display_links = ("created_at", "mobile_phone")
    readonly_fields = ("created_at", "mobile_phone", "verified", "code")
    search_fields = ("mobile_phone",)


class SMSTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "content")
    list_editable = ("content",)


admin.site.register(SMSMessage, SMSMessageAdmin)
admin.site.register(SMSTemplate, SMSTemplateAdmin)
admin.site.register(OTP, OTPAdmin)
