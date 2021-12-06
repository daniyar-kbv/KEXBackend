from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (_("Personal info"), {
            "fields": (
                'mobile_phone',
                'name',
                "email",
                "password",
            )}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    'groups'
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields":
            (
                "mobile_phone",
                "password1",
                "password2",
                "is_staff",
            ),}),
    )
    readonly_fields = "last_login", "created_at", "updated_at", 'mobile_phone'
    list_display = 'mobile_phone', "name", "is_staff", "is_active"
    search_fields = "mobile_phone",
    ordering = 'mobile_phone',
    list_filter = 'is_staff',


admin.site.register(User, UserAdmin)
