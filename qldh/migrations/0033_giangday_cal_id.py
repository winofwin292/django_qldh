# Generated by Django 4.0.1 on 2022-04-05 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qldh', '0032_alter_giangday_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='giangday',
            name='cal_id',
            field=models.TextField(default=''),
        ),
    ]
