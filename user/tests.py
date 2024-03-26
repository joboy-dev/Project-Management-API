from rest_framework.test import APITestCase

from .models import CustomUser
from . import serializers

class CreateAccountTest(APITestCase):
    '''Test to create an account for a user'''
    
    
