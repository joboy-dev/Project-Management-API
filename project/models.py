import datetime
from django.db import models
from uuid import uuid4
from user.models import CustomUser

from workspace.models import Member, Workspace

class Project(models.Model):
    '''Project model'''

    id = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(null=False, max_length=40, unique=True)
    description = models.CharField(null=False, max_length=255)
    start_date = models.DateTimeField(null=False, default=datetime.datetime.now())
    end_date = models.DateTimeField(null=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, null=True)
    members = models.ManyToManyField(Member, related_name='projects', blank=True)
    created_by = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.id} | {self.name} | {self.workspace.name}'
    