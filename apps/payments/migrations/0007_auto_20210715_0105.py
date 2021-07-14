# Generated by Django 3.1.7 on 2021-07-14 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_auto_20210715_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_type',
            field=models.CharField(choices=[('DEBIT_CARD', 'Оплата дебетовой картой'), ('GOOGLE_PAY', 'Оплата через GooglePay'), ('APPLE_PAY', 'Оплата через ApplePay')], max_length=256),
        ),
    ]
