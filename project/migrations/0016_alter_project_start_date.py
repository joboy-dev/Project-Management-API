# Generated by Django 5.0.1 on 2024-02-05 13:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0015_alter_project_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 5, 14, 53, 13, 558538)),
        ),
    ]
