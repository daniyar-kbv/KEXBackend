# Generated by Django 3.1.7 on 2021-06-15 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20210614_2102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartposition',
            name='cart',
        ),
    ]
