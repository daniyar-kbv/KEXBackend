# Generated by Django 3.1.7 on 2021-07-16 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210619_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.CharField(choices=[('kk', 'Казахский'), ('ru', 'Русский'), ('en', 'Английский')], default='ru', max_length=20, verbose_name='Язык'),
        ),
    ]
