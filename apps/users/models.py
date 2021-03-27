import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField


from .managers import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    mobile_phone = PhoneNumberField("Моб. телефон", unique=True)
    is_active = models.BooleanField("Активный", default=True)
    is_staff = models.BooleanField("Сотрудник", default=False)

    secret_key = models.UUIDField("Секретный ключ", default=uuid.uuid4, unique=True)

    created_at = models.DateTimeField("Создан", default=timezone.now)
    updated_at = models.DateTimeField("Обновлен", auto_now=True)

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
        verbose_name = "Учетная запись"
        verbose_name_plural = "Учетная запись"

    def __str__(self):
        return f"{self._meta.verbose_name} {str(self.pk)} ({self.mobile_phone})"

    def get_username(self):
        return self.mobile_phone
