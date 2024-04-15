from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model
from datetime import datetime as dt

User = get_user_model()

# Create your models here.
class Notification(models.Model):
    '''Notification model'''
    
    id = models.UUIDField(default=uuid4, primary_key=True)
    message = models.CharField(null=False, max_length=300)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='receiver')
    date_sent = models.DateTimeField(auto_now_add=True)
    