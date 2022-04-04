# Generated by Django 3.2 on 2021-04-22 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qldh', '0012_auto_20210422_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diemso',
            name='mon',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qldh.monhoc'),
        ),
        migrations.AlterField(
            model_name='diemso',
            name='nam_hoc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qldh.namhoc'),
        ),
        migrations.AlterField(
            model_name='giangday',
            name='ma_lop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qldh.lophoc'),
        ),
        migrations.AlterField(
            model_name='giangday',
            name='nam_hoc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qldh.namhoc'),
        ),
        migrations.AlterField(
            model_name='hocsinh',
            name='lop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='qldh.lophoc'),
        ),
        migrations.AlterField(
            model_name='ketquahoctap',
            name='nam_hoc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qldh.namhoc'),
        ),
    ]