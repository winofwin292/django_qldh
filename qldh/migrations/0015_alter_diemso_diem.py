# Generated by Django 3.2 on 2021-05-06 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qldh', '0014_auto_20210502_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diemso',
            name='diem',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
