# Generated by Django 3.1.7 on 2021-06-14 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_cartposition_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartposition',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='orders.cart', to_field='uuid'),
        ),
    ]
