# Generated by Django 3.2 on 2021-04-22 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qldh', '0008_lophoc_nam_hoc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lophoc',
            name='nam_hoc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='qldh.namhoc', to_field='mo_ta'),
        ),
    ]
