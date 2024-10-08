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
    class Meta:
        verbose_name = _("Учетная запись")
        verbose_name_plural = _("Учетная запись")

    mobile_phone = PhoneNumberField(_("Моб. телефон"), unique=True)
    name = models.CharField(_("Имя"), max_length=256, null=True)
    email = models.EmailField(null=True)

    language = models.CharField(_("Язык"), max_length=20, choices=Languages.choices, default=settings.DEFAULT_LANGUAGE)
    is_active = models.BooleanField(_("Активный"), default=True)
    is_staff = models.BooleanField(_("Сотрудник"), default=False)
    secret_key = models.UUIDField(_("Секретный ключ"), default=uuid.uuid4, unique=True)
    device_uuid = models.UUIDField(_("UUID устройства"), default=uuid.uuid4, unique=True)

    created_at = models.DateTimeField(_("Создан"), default=timezone.now)
    updated_at = models.DateTimeField(_("Обновлен"), auto_now=True)

    USERNAME_FIELD = "mobile_phone"

    objects = UserManager()

    def __str__(self):
        return f"{self._meta.verbose_name} {str(self.pk)} ({self.mobile_phone})"

    def update_device_uuid(self):
        self.device_uuid = uuid.uuid4()
        self.save(update_fields=["device_uuid"])

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

    def get_username(self):
        return self.mobile_phone

    def add_new_address(self, address, local_brand) -> None:
        self.addresses.create(
            address=address, local_brand=local_brand
        )

    @staticmethod
    def set_current_address(user_address) -> None:
        user_address.save()

    @staticmethod
    def change_address_brand(user_address, local_brand) -> None:
        user_address.local_brand = local_brand
        user_address.save()

    @property
    def current_address(self):
        return self.addresses.first()

    @property
    def current_address_pk(self):
        if self.addresses.exists():
            return self.addresses.first().pk

    @property
    def last_payment_type(self):
        if self.payments.exists():
            return self.payments.last().payment_type

    @property
    def get_all_debit_cards(self):
        return self.debit_cards.active()

    @property
    def current_debit_card(self):
        return self.debit_cards.active().first()

    @property
    def current_debit_card_pk(self):
        if self.debit_cards.active().exists():
            return self.debit_cards.active().first().pk

    @property
    def fb_token(self):
        return self.fb_tokens[-1] if self.fb_tokens else None

    @property
    def fb_tokens(self):
        return [fb.token for fb in self.firebase_tokens.all()]


class UserAddress(TimestampModel):
    class Meta:
        ordering = ("-updated_at",)

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
    local_brand = models.ForeignKey(
        "partners.LocalBrand",
        on_delete=models.PROTECT,
        null=True,
    )
