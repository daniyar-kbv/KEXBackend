# Generated by Django 3.1.7 on 2021-06-15 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_auto_20210615_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='location.city', verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='location.country', verbose_name='Страна'),
        ),
    ]
