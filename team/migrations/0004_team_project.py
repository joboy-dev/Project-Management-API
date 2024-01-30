# Generated by Django 5.0.1 on 2024-01-29 22:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_remove_project_teams_alter_project_start_date'),
        ('team', '0003_alter_team_team_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.project'),
        ),
    ]
