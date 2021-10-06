# Generated by Django 3.1.7 on 2021-07-16 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0011_auto_20210716_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='acs_url',
            field=models.URLField(max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='pa_req',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='pa_res',
            field=models.CharField(max_length=512, null=True),
        ),
    ]
