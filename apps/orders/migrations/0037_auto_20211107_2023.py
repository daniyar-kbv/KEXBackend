# Generated by Django 3.1.7 on 2021-11-07 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0036_auto_20211002_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('NEW', 'Новый заказ'), ('PAID', 'Оплачено'), ('APPLYING', 'Процесс просадки в IIKO'), ('APPLY_ERROR', 'Ошибка при просадке в IIKO'), ('APPLIED', 'Просажено в IIKO'), ('UNCONFIRMED', 'Заказ подтверждается'), ('READY_FOR_COOKING', 'Заказ готов к приготовлению'), ('COOKING_STARTED', 'Заказ в процессе готовки'), ('COOKING_COMPLETED', 'Заказ приготовлен'), ('WAITING', 'Ожидание доставки заказа'), ('ON_WAY', 'Заказ доставляется'), ('DELIVERED', 'Заказ доставлен'), ('DONE', 'Заказ завершен'), ('CANCELLED', 'Заказ отменен в IIKO')], default='NEW', max_length=32, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='orderstatustransition',
            name='status',
            field=models.CharField(choices=[('NEW', 'Новый заказ'), ('PAID', 'Оплачено'), ('APPLYING', 'Процесс просадки в IIKO'), ('APPLY_ERROR', 'Ошибка при просадке в IIKO'), ('APPLIED', 'Просажено в IIKO'), ('UNCONFIRMED', 'Заказ подтверждается'), ('READY_FOR_COOKING', 'Заказ готов к приготовлению'), ('COOKING_STARTED', 'Заказ в процессе готовки'), ('COOKING_COMPLETED', 'Заказ приготовлен'), ('WAITING', 'Ожидание доставки заказа'), ('ON_WAY', 'Заказ доставляется'), ('DELIVERED', 'Заказ доставлен'), ('DONE', 'Заказ завершен'), ('CANCELLED', 'Заказ отменен в IIKO')], default='NEW', max_length=20, verbose_name='Статус'),
        ),
    ]
