# Generated by Django 3.1.7 on 2021-05-23 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0019_auto_20210512_1640'),
        ('nomenclature', '0004_remove_position_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='merchant',
        ),
        migrations.AddField(
            model_name='category',
            name='iiko_brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='partners.iikobrand', verbose_name='Бренд'),
        ),
        migrations.AddField(
            model_name='position',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='positions', to='nomenclature.category', verbose_name='Категория'),
        ),
    ]
