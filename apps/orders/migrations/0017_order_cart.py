# Generated by Django 3.1.7 on 2021-07-14 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_ratedorder_ratesample_ratestar'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order', to='orders.cart'),
        ),
    ]
