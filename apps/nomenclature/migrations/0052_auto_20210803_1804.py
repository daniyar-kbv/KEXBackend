# Generated by Django 3.1.7 on 2021-08-03 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclature', '0051_positionmodifiergroup_modifier_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='positionmodifiergroup',
            old_name='position',
            new_name='branch_position',
        ),
    ]
