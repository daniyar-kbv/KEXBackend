# Generated by Django 3.1.7 on 2021-10-31 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0028_auto_20211031_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='kml_map',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
