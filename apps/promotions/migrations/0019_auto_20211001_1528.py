# Generated by Django 3.1.7 on 2021-10-01 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0018_auto_20210917_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='slug',
            field=models.SlugField(blank=True, unique=True, verbose_name='Читабельная ссылка'),
        ),
    ]
