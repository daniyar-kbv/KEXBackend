# Generated by Django 3.1.7 on 2021-05-23 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0019_auto_20210512_1640'),
        ('nomenclature', '0009_auto_20210523_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='positions', to='partners.organization'),
        ),
    ]
