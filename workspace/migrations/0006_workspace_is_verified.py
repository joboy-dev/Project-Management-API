# Generated by Django 5.0.1 on 2024-01-26 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0005_alter_member_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='workspace',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]