# Generated by Django 3.1.7 on 2021-06-21 03:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('translations', '0006_auto_20210612_0104'),
        ('nomenclature', '0032_branchpositionprices_branchsize'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BranchSize',
            new_name='PositionSize',
        ),
    ]
