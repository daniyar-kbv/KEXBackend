# Generated by Django 3.1.7 on 2021-09-17 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclature', '0088_auto_20210914_1322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='position',
            old_name='image',
            new_name='image_big',
        ),
        migrations.AddField(
            model_name='position',
            name='image_small',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
