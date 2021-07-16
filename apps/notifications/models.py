from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from apps.common.models import AbstractTitleModel, AbstractDescriptionModel, MultipleModelFK, UUIDModel
from apps.notifications import PushTypes
from apps.orders.models import Lead

User = get_user_model()


class Notification(UUIDModel, AbstractTitleModel, AbstractDescriptionModel, MultipleModelFK):
    push_type = models.CharField(
        max_length=255,
        verbose_name="Тип",
        choices=PushTypes.choices,
        default=PushTypes.INFO
    )
    date = models.DateTimeField(verbose_name="Дата", null=True, default=timezone.now)

    class Meta:
        verbose_name = "Пуш уведомление"
        verbose_name_plural = "Пуш уведомления"


class FirebaseToken(models.Model):
    token = models.CharField("Firebase token", max_length=255, blank=True, null=True)
    lead = models.ForeignKey(Lead, verbose_name="Лид", on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="firebase_token"
    )

    class Meta:
        verbose_name = "Токен Firebase"
        verbose_name_plural = "Токены Firebase"
