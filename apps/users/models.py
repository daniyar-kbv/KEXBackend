import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _  # noqa
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField


from .managers import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    mobile_phone = PhoneNumberField(_("Моб. телефон"), unique=True)
    name = models.CharField(_("Имя"), max_length=256, null=True)
    email = models.EmailField(null=True)

    is_active = models.BooleanField(_("Активный"), default=True)
    is_staff = models.BooleanField(_("Сотрудник"), default=False)

    secret_key = models.UUIDField(_("Секретный ключ"), default=uuid.uuid4, unique=True)

    created_at = models.DateTimeField(_("Создан"), default=timezone.now)
    updated_at = models.DateTimeField(_("Обновлен"), auto_now=True)

    USERNAME_FIELD = "mobile_phone"

    objects = UserManager()

    def clean(self):
        pass

    def has_perm(self, perm, obj=None):
        if not self.is_active:
            return False

        if self.is_superuser:
            return True

        return perm in self.get_all_permissions(obj)

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        return self.is_active and any(
            perm[: perm.index(".")] == app_label for perm in self.get_all_permissions()
        )

    class Meta:
        verbose_name = _("Учетная запись")
        verbose_name_plural = _("Учетная запись")

    def __str__(self):
        return f"{self._meta.verbose_name} {str(self.pk)} ({self.mobile_phone})"

    def get_username(self):
        return self.mobile_phone
