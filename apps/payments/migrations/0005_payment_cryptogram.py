# Generated by Django 3.1.7 on 2021-07-14 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_auto_20210714_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='cryptogram',
            field=models.CharField(default='', max_length=1024),
            preserve_default=False,
        ),
    ]
