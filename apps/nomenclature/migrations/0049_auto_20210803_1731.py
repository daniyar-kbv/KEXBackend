# Generated by Django 3.1.7 on 2021-08-03 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclature', '0048_auto_20210626_1138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modifiergroup',
            name='is_required',
        ),
        migrations.RemoveField(
            model_name='modifiergroup',
            name='max_amount',
        ),
        migrations.RemoveField(
            model_name='modifiergroup',
            name='min_amount',
        ),
        migrations.RemoveField(
            model_name='modifiergroup',
            name='positions',
        ),
        migrations.CreateModel(
            name='PositionModifierGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_amount', models.PositiveSmallIntegerField(default=0)),
                ('max_amount', models.PositiveSmallIntegerField(default=0)),
                ('is_required', models.BooleanField(default=False)),
                ('modifier_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position_modifier_groups', to='nomenclature.modifiergroup')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position_modifier_groups', to='nomenclature.branchposition')),
            ],
        ),
    ]
