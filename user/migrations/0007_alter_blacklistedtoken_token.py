# Generated by Django 5.0.1 on 2024-01-25 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_blacklistedtoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blacklistedtoken',
            name='token',
            field=models.CharField(max_length=1000, unique=True),
        ),
    ]
