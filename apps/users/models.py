import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _  # noqa
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import TimestampModel
from django.conf import settings
from config.settings import Languages

from .managers import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    mobile_phone = PhoneNumberField(_("Моб. телефон"), unique=True)
    name = models.CharField(_("Имя"), max_length=256, null=True)
    email = models.EmailField(null=True)

    language = models.CharField(_("Язык"), max_length=20, choices=Languages.choices, default=settings.DEFAULT_LANGUAGE)
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

    @property
    def fb_token(self):
        return self.firebase_token.token

    def set_is_current_false(self, current_pk: int) -> None:
        self.addresses.exclude(pk=current_pk).update(is_current=False)

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

    def add_new_address(self, address, local_brand) -> None:
        self.addresses.get_or_create(
            address=address,
            defaults={
                "is_current": True,
                "local_brand": local_brand,
            },
        )

    def set_current_address(self, user_address) -> None:
        ...

    @property
    def current_address(self):
        return self.addresses.filter(is_current=True).last()


class UserAddress(TimestampModel):
    class Meta:
        ordering = "created_at",

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="addresses"
    )
    address = models.ForeignKey(
        "location.Address",
        on_delete=models.CASCADE,
        null=True,
    )
    is_current = models.BooleanField(
        _("Текущий адрес"),
        default=False,
    )
    local_brand = models.ForeignKey(
        "partners.LocalBrand",
        on_delete=models.PROTECT,
        null=True,
    )
