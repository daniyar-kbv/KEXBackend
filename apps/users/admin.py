# from django.contrib import admin
# from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import Group
# from django.utils.translation import gettext_lazy as _
#
# from .models import User
#
# admin.site.unregister(Group)
#
#
# class UserAdmin(BaseUserAdmin):
#     fieldsets = (
#         (_("Personal info"), {
#             "fields": (
#                 "email",
#                 "password",
#                 "first_name",
#                 "last_name",
#                 "middle_name"
#             )}),
#         (
#             _("Permissions"),
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     "is_credit_manager"
#                 ),
#             },
#         ),
#         (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
#     )
#     add_fieldsets = (
#         (None, {"classes": ("wide",), "fields":
#             (
#                 "email",
#                 "password1",
#                 "password2",
#                 "is_credit_manager",
#                 "is_supervisor",
#             ),}),
#     )
#     readonly_fields = ("last_login", "created_at", "updated_at")
#     list_display = ("__str__", "full_name", "is_staff", "is_active")
#     search_fields = ("email", "person__iin")
#     ordering = ("email",)
#     list_filter = ("is_credit_manager", "is_staff")
#
#     def get_fieldsets(self, request, obj=None):
#         fieldsets = super().get_fieldsets(request, obj)
#         if obj and (obj.is_credit_manager or obj.is_supervisor):
#             return (*fieldsets, (_("Manager info"), {
#                 "fields": ("merchant", "branch")
#             }))
#
#         return fieldsets
#
#
# admin.site.register(User, UserAdmin)
