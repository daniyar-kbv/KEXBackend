# Generated by Django 3.1.7 on 2021-09-28 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0028_lead_delivery_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ratesample',
            name='name',
        ),
        migrations.RemoveField(
            model_name='ratestar',
            name='description',
        ),
        migrations.RemoveField(
            model_name='ratestar',
            name='rate_samples',
        ),
        migrations.RemoveField(
            model_name='ratestar',
            name='title',
        ),
        migrations.DeleteModel(
            name='RatedOrder',
        ),
        migrations.DeleteModel(
            name='RateSample',
        ),
        migrations.DeleteModel(
            name='RateStar',
        ),
    ]
