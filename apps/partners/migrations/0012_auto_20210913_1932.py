# Generated by Django 3.1.7 on 2021-09-13 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0011_branch_is_alive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Активна в системе mti'),
        ),
        migrations.AlterField(
            model_name='localbrand',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Активна в системе mti'),
        ),
    ]
