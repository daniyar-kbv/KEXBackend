# Generated by Django 3.1.7 on 2021-06-11 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0004_auto_20210611_0804'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promotion',
            options={},
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='image',
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='position',
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='template',
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='type',
        ),
    ]
