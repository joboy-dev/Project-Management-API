import os

from django.db import models
from uuid import uuid4

from project.models import Project
from user.models import CustomUser
from workspace.models import Member

# Create your models here.
class Team(models.Model):
    '''Team model'''
    
    def upload_image(model, filename):
        '''Function to upload image and save in a folder for each object'''
        
        extension = filename.split('.')[-1]
        return os.path.join('team', str(model.id), f'team_pic.{extension}')
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=120, null=False, unique=True)
    team_pic = models.ImageField(upload_to=upload_image, null=True)
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    members = models.ManyToManyField(Member, related_name='teams', blank=True)
    created_by = models.ForeignKey(Member, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.id} | {self.name} | {self.project.name}'