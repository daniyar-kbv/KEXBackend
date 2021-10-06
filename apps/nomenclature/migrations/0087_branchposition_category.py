# Generated by Django 3.1.7 on 2021-09-13 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclature', '0086_remove_branchposition_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='branchposition',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='branch_positions', to='nomenclature.category', to_field='uuid'),
        ),
    ]
