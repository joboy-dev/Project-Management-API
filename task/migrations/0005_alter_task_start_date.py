# Generated by Django 5.0.1 on 2024-03-20 09:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_alter_task_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 20, 10, 33, 49, 659617)),
        ),
    ]
