# Generated by Django 5.0.1 on 2024-01-26 21:22

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0009_alter_member_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
