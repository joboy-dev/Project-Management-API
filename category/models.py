from django.db import models
from uuid import uuid4

# Create your models here.
class Category(models.Model):
    '''Category model'''
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=50, unique=True, null=False)
    descriptionn= models.CharField(max_length=255, null=False)
    label_color = models.CharField(max_length=25, null=False)
    is_team_category = models.BooleanField(default=False, null=False)
    
    def __str__(self):
        return f'{self.id} | {self.name}'
        