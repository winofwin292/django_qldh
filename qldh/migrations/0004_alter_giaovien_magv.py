# Generated by Django 3.2 on 2021-04-20 16:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qldh', '0003_alter_giaovien_magv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giaovien',
            name='magv',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]
