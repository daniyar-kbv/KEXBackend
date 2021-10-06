# Generated by Django 3.1.7 on 2021-06-04 14:20

from django.db import migrations, models
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SMSMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Время последнего изменения')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Идентификатор')),
                ('recipients', models.CharField(editable=False, max_length=255, verbose_name='Получатели')),
                ('content', models.TextField(editable=False, verbose_name='Содержимое')),
                ('error_code', models.IntegerField(editable=False, null=True, verbose_name='Код ошибки')),
                ('error_description', models.CharField(editable=False, max_length=255, null=True, verbose_name='Описание ошибки')),
            ],
            options={
                'verbose_name': 'SMS сообщение',
                'verbose_name_plural': 'SMS сообщения',
            },
        ),
        migrations.CreateModel(
            name='SMSTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('OTP', 'Отправка одноразового пароля')], max_length=32, unique=True, verbose_name='Наименование')),
                ('content', models.TextField(verbose_name='Содержимое')),
            ],
            options={
                'verbose_name': 'Шаблон СМС',
                'verbose_name_plural': 'Шаблоны СМС',
            },
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Время последнего изменения')),
                ('code', models.CharField(db_index=True, editable=False, max_length=12, verbose_name='OTP')),
                ('verified', models.BooleanField(default=False, editable=False, verbose_name='Подтверждён')),
                ('mobile_phone', phonenumber_field.modelfields.PhoneNumberField(editable=False, max_length=128, region=None, verbose_name='Мобильный телефон')),
            ],
            options={
                'verbose_name': 'Одноразовый пароль',
                'verbose_name_plural': 'Одноразовые пароли',
                'unique_together': {('code', 'mobile_phone')},
            },
        ),
    ]
