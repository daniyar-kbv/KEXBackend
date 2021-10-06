# Generated by Django 3.1.7 on 2021-06-04 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('translations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(blank=True, max_length=255, null=True, verbose_name='Страна')),
                ('region', models.CharField(blank=True, max_length=255, null=True, verbose_name='Регион')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='Город')),
                ('district', models.CharField(blank=True, max_length=255, null=True, verbose_name='Район')),
                ('street', models.CharField(blank=True, max_length=255, null=True, verbose_name='Улица')),
                ('building', models.CharField(blank=True, max_length=100, null=True, verbose_name='Дом / здание')),
                ('corpus', models.CharField(blank=True, max_length=100, null=True, verbose_name='Корпус')),
                ('flat', models.CharField(blank=True, max_length=50, null=True, verbose_name='Квартира')),
                ('postal_code', models.CharField(blank=True, max_length=7, null=True, verbose_name='Почтовый индекс')),
                ('longitude', models.DecimalField(decimal_places=8, max_digits=12, null=True, verbose_name='Долгота')),
                ('latitude', models.DecimalField(decimal_places=8, max_digits=12, null=True, verbose_name='Широта')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(blank=True, max_length=32, null=True, verbose_name='Код страны')),
                ('name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='translations.multilanguagechar', verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cities', to='location.country', verbose_name='Страна')),
                ('name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='translations.multilanguagechar', verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'unique_together': {('country', 'name')},
            },
        ),
    ]
