from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4

User = get_user_model()

class Workspace(models.Model):
    '''Workspace model'''
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=128, null=False, unique=True)
    company_email = models.EmailField(null=False, unique=True)
    no_of_members_allowed = models.IntegerField(null=False)
    current_no_of_members = models.IntegerField(null=False, default=0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
  

class Member(models.Model):
    '''Member model for workspace and projects etc'''
    
    VIEWER = 'viewer'
    EDITOR = 'editor'
    roles = [
        (VIEWER, 'Viewer'),
        (EDITOR, 'Editor'),
    ]
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    role = models.CharField(choices=roles, default=VIEWER, max_length=6)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.id} | {self.user.email} | {self.workspace.name} | {self.role}"
    
    class Meta:
        ordering = ['workspace']