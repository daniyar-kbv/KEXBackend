# Generated by Django 3.1.7 on 2021-09-15 09:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0013_auto_20210914_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branch',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='branch',
            name='start_time',
        ),
        migrations.CreateModel(
            name='BranchDeliveryTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_type', models.CharField(choices=[('DAY_DELIVERY', 'Дневная доставка'), ('NIGHT_DELIVERY', 'Ночная доставка')], max_length=256)),
                ('start_time', models.TimeField(default=datetime.time(10, 0), verbose_name='Время работы с')),
                ('end_time', models.TimeField(default=datetime.time(22, 0), verbose_name='Время работы до')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_times', to='partners.branch')),
            ],
        ),
    ]
