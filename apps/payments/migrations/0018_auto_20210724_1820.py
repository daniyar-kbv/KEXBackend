# Generated by Django 3.1.7 on 2021-07-24 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0017_remove_debitcard_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='debitcard',
            options={'ordering': ('-updated_at',)},
        ),
    ]
