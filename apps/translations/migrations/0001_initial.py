# Generated by Django 3.1.7 on 2021-05-21 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MultiLanguageChar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_ru', models.CharField(max_length=256, null=True, verbose_name='Текст (рус)')),
                ('text_kk', models.CharField(blank=True, max_length=256, null=True, verbose_name='Текст (каз)')),
                ('text_en', models.CharField(blank=True, max_length=256, null=True, verbose_name='Текст (англ)')),
            ],
        ),
    ]
