# Generated by Django 3.1.7 on 2021-08-03 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclature', '0050_auto_20210803_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='positionmodifiergroup',
            name='modifier_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='position_modifier_groups', to='nomenclature.modifiergroup', to_field='uuid'),
        ),
    ]
