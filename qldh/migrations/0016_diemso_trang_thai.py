# Generated by Django 3.2 on 2021-05-06 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qldh', '0015_alter_diemso_diem'),
    ]

    operations = [
        migrations.AddField(
            model_name='diemso',
            name='trang_thai',
            field=models.CharField(default='Chưa nhập', max_length=50),
        ),
    ]