# Generated by Django 3.1.7 on 2021-05-27 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0019_auto_20210512_1640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='name',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='name',
        ),
    ]
