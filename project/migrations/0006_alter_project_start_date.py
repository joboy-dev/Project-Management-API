# Generated by Django 5.0.1 on 2024-01-29 22:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_alter_project_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 29, 23, 26, 33, 902187)),
        ),
    ]
