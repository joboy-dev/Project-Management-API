# Generated by Django 5.0.1 on 2024-01-24 16:20

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_customuser_verification_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='verification_token',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
