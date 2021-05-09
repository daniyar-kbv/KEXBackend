# Generated by Django 3.1.7 on 2021-05-09 19:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0015_auto_20210504_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='end_time',
            field=models.TimeField(default=datetime.time(22, 0), verbose_name='Время работы до'),
        ),
        migrations.AddField(
            model_name='organization',
            name='start_time',
            field=models.TimeField(default=datetime.time(10, 0), verbose_name='Время работы с'),
        ),
    ]
