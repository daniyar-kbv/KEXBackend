# Generated by Django 3.1.7 on 2021-09-14 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0012_auto_20210913_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='is_alive',
            field=models.BooleanField(default=False, verbose_name='Доступен в системе IIKO'),
        ),
    ]
