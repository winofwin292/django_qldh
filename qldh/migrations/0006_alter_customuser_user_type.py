# Generated by Django 3.2 on 2021-04-20 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qldh', '0005_auto_20210420_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.IntegerField(choices=[(1, 'Admin'), (2, 'Giáo Viên'), (3, 'Học Sinh')], default=1),
        ),
    ]
