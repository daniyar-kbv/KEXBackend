# Generated by Django 3.1.7 on 2021-07-24 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0016_auto_20210717_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='debitcard',
            name='is_active',
        ),
    ]
