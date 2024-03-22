from django.db import models
from uuid import uuid4

from project.models import Project
from workspace.models import Member

# Create your models here.
class Comment(models.Model):
    '''Comment model'''
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    comment = models.CharField(null=False, max_length=300)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name='project')
    commenter = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='member')
    
    def __str__(self):
        return  f'Comment by {self.commenter.user.email} on {self.project.name}'
    

class CommentReply(models.Model):
    '''Comment reply model'''
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    reply = models.CharField(null=False, max_length=300)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, related_name='comment_obj')
    commenter = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='member_commenter')
    