from django.db import models
import datetime
from uuid import uuid4

from project.models import Project
from team.models import Team
from workspace.models import Member

# Create your models here.
class Task(models.Model):
    '''Task model'''
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=128, unique=True, null=False)
    description = models.CharField(null=False, max_length=255)
    label_color = models.CharField(max_length=25, null=False, default='0xFFFFFFFF')
    is_complete = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=False, default=datetime.datetime.now())
    end_date = models.DateTimeField(null=True)
    is_team_task = models.BooleanField(default=False)
    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    members = models.ManyToManyField(Member, related_name='tasks', blank=True)
    created_by = models.ForeignKey(Member, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.id} | {self.name} | {self.project.name}'