# Generated by Django 3.1.7 on 2021-05-27 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_descriptionfield_namefield_testcountry_testmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='descriptionfield',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='namefield',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='testcountry',
            name='extra',
        ),
        migrations.RemoveField(
            model_name='testcountry',
            name='name',
        ),
        migrations.DeleteModel(
            name='TestModel',
        ),
        migrations.DeleteModel(
            name='DescriptionField',
        ),
        migrations.DeleteModel(
            name='NameField',
        ),
        migrations.DeleteModel(
            name='TestCountry',
        ),
    ]
