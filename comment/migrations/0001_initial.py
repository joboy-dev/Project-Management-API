# Generated by Django 4.1.13 on 2024-04-10 14:46

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workspace', '0010_alter_member_id'),
        ('project', '0024_alter_project_start_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('comment', models.CharField(max_length=300)),
                ('commenter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member', to='workspace.member')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='project.project')),
            ],
        ),
        migrations.CreateModel(
            name='CommentReply',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('reply', models.CharField(max_length=300)),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_obj', to='comment.comment')),
                ('commenter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='member_commenter', to='workspace.member')),
            ],
        ),
    ]
