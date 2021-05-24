# Generated by Django 3.1.7 on 2021-05-21 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('translations', '0001_initial'),
        ('nomenclature', '0002_auto_20210415_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='translations.multilanguagechar', verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='combo',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='translations.multilanguagechar', verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='position',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='translations.multilanguagechar', verbose_name='Название'),
        ),
    ]
