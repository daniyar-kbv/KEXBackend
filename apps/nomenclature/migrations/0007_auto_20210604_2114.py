# Generated by Django 3.1.7 on 2021-06-04 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclature', '0006_auto_20210604_2111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='position',
            old_name='brand',
            new_name='local_brand',
        ),
    ]
