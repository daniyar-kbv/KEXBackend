# Generated by Django 3.1.7 on 2021-08-13 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('translations', '0006_auto_20210612_0104'),
        ('partners', '0011_branch_is_alive'),
        ('nomenclature', '0059_auto_20210813_1628'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LocalPosition',
            new_name='Position',
        ),
    ]
