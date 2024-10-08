# Generated by Django 3.1.7 on 2021-08-15 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclature', '0068_positionmodifiergroup_uuid'),
        ('orders', '0025_cartpositionmodifiergroup_position_modifier_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartpositionmodifier',
            name='branch_position',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='nomenclature.branchposition', to_field='uuid'),
        ),
    ]
