# Generated by Django 3.1.7 on 2021-09-28 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('translations', '0006_auto_20210612_0104'),
        ('orders', '0029_auto_20210928_1528'),
    ]

    operations = [
        migrations.CreateModel(
            name='RateSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='translations.multilanguagechar', verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Шаблон оценки',
                'verbose_name_plural': 'Шаблоны оценки',
            },
        ),
        migrations.CreateModel(
            name='RateStar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveSmallIntegerField(default=1, verbose_name='Значение')),
                ('description', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='translations.multilanguagetext', verbose_name='Описание')),
                ('rate_samples', models.ManyToManyField(blank=True, to='order_rates.RateSample', verbose_name='Шаблоны оценки')),
                ('title', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='translations.multilanguagechar', verbose_name='Заголовок')),
            ],
            options={
                'verbose_name': 'Звезда оценки',
                'verbose_name_plural': 'Звезды оценки',
                'ordering': ['value'],
            },
        ),
        migrations.CreateModel(
            name='RatedOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates', to='orders.order', verbose_name='Заказ')),
                ('rate_samples', models.ManyToManyField(blank=True, to='order_rates.RateSample', verbose_name='Шаблоны оценки')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_rates.ratestar', verbose_name='Звезда')),
            ],
            options={
                'verbose_name': 'Оценка заказа',
                'verbose_name_plural': 'Оценки заказов',
            },
        ),
    ]
