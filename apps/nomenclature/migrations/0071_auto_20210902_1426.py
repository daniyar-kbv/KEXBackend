# Generated by Django 3.1.7 on 2021-09-02 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclature', '0070_auto_20210902_1411'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branchposition',
            options={'ordering': ('position__priority',)},
        ),
        migrations.AddField(
            model_name='position',
            name='priority',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
