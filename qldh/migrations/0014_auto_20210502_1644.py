# Generated by Django 3.2 on 2021-05-02 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qldh', '0013_auto_20210422_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giangday_chitiet',
            name='buoi',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='giangday_chitiet',
            name='so_tiet',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='giangday_chitiet',
            name='thu',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='giangday_chitiet',
            name='tiet_bd',
            field=models.CharField(default='', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='giangday_chitiet',
            name='tiet_kt',
            field=models.CharField(default='', max_length=2, null=True),
        ),
    ]
