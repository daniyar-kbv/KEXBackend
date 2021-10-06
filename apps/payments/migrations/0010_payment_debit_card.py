# Generated by Django 3.1.7 on 2021-07-16 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0009_remove_payment_debit_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='debit_card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='payments.debitcard', to_field='uuid'),
        ),
    ]
