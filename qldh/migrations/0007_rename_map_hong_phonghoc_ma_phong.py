# Generated by Django 3.2 on 2021-04-21 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qldh', '0006_alter_customuser_user_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='phonghoc',
            old_name='map_hong',
            new_name='ma_phong',
        ),
    ]
