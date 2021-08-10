# Generated by Django 3.1.7 on 2021-08-09 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0015_promotion_web_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='end_date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Дата завершения'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='start_date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Дата начала'),
        ),
    ]
