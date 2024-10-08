# Generated by Django 3.1.7 on 2021-09-09 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclature', '0073_remove_position_is_additional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='position_type',
            field=models.CharField(choices=[('DISH', 'Основное блюдо'), ('MODIFIER', 'Модификатор'), ('ADDITIONAL', 'Дополнительное блюдо'), ('DAY_DELIVERY', 'Дневная доставка'), ('NIGHT_DELIVERY', 'Ночная доставка')], default='DISH', max_length=256),
        ),
    ]
