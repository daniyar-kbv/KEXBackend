# Generated by Django 3.1.7 on 2021-11-02 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclature', '0094_remove_modifiergroup_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='modifiergroup',
            name='name',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
