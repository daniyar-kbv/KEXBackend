# Generated by Django 3.1.7 on 2021-05-27 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0007_auto_20210510_0142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='name',
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='city',
            name='name',
        ),
    ]
