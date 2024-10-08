# Generated by Django 3.1.7 on 2021-06-25 21:45

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('translations', '0006_auto_20210612_0104'),
        ('nomenclature', '0041_auto_20210626_0343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branchpositionmodifier',
            name='is_required',
        ),
        migrations.RemoveField(
            model_name='branchpositionmodifier',
            name='max_amount',
        ),
        migrations.RemoveField(
            model_name='branchpositionmodifier',
            name='min_amount',
        ),
        migrations.CreateModel(
            name='ModifierGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Идентификатор')),
                ('iiko_name', models.CharField(max_length=255)),
                ('min_amount', models.PositiveSmallIntegerField(default=0)),
                ('max_amount', models.PositiveSmallIntegerField(default=0)),
                ('is_required', models.BooleanField(default=False)),
                ('outer_id', models.UUIDField(null=True)),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='translations.multilanguagechar', verbose_name='Название')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='branchpositionmodifier',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nomenclature.modifiergroup'),
        ),
        migrations.DeleteModel(
            name='PositionGroup',
        ),
    ]
