# Generated by Django 3.1.7 on 2021-06-04 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0004_auto_20210604_2034'),
        ('nomenclature', '0004_auto_20210604_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branchcategory',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='categories', to='partners.branch', verbose_name='Филиал'),
        ),
        migrations.AlterField(
            model_name='category',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='categories', to='partners.brand', verbose_name='Бренд'),
        ),
        migrations.AlterField(
            model_name='localcategory',
            name='local_brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='categories', to='partners.localbrand', verbose_name='Локальный бренд'),
        ),
    ]
