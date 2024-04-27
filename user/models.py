from datetime import datetime, timezone
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy
from uuid import uuid4

from .manager import CustomUserManager

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    '''Custom user model'''
    
    def upload_image(model, filename):
        '''Function to upload image and save in a folder for each object'''
        extension = filename.split('.')[-1]
        return os.path.join('user', str(model.id), f'user_pic.{extension}')
    
    # Subscription
    STARTER = 'starter'
    PRO = 'pro'
    ULTIMATE = 'ultimate'
    
    subscription_choices = [
        (STARTER, 'Starter'),
        (PRO, 'Pro'),
        (ULTIMATE, 'Ultimate'),
    ]

    id = models.UUIDField(default=uuid4, primary_key=True)
    email = models.EmailField(gettext_lazy('email address'), unique=True, null=False)
    first_name = models.CharField(max_length=128, null=False)
    last_name = models.CharField(max_length=128, null=False)
    profile_pic = models.ImageField(default='user/default.png', upload_to=upload_image, null=True)
    phone_number = models.CharField(max_length=11, null=False)
    is_verified = models.BooleanField(default=False)
    subscription_plan = models.CharField(choices=subscription_choices, default=STARTER, null=False, max_length=10)
    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Token(models.Model):
    '''A model to store user access tokens'''
    
    token = models.CharField(max_length=500)
    user = models.ForeignKey(CustomUser, related_name="user_token", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.email}'

    class Meta:
        unique_together = ("token", "user")
        

class BlacklistedToken(models.Model):
    '''A model to store blacklisted tokens'''
    
    token = models.CharField(max_length=500)
    user = models.ForeignKey(CustomUser, related_name="token_user", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    expiration_date = models.DateTimeField()

    def is_expired(self):
        return self.expiration_date.replace(tzinfo=None) < datetime.now().replace(tzinfo=None)
    
    def __str__(self):
        return f'{self.user.email}'

    class Meta:
        unique_together = ("token", "user")
        