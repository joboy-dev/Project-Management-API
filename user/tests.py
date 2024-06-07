from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, Token
from .import serializers


def authorize(client):
    '''Function to authorize the user'''
    
    token = Token.objects.get(user__email='test@gmail.com')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.token}')
    

class RegisterTestCase(APITestCase):
    '''Test to create an account for a user'''
    
    def test_register(self):
        data = {
            'email': 'test@gmail.com', 
            'first_name': 'test', 
            'last_name': 'tester', 
            'password': 'Testing@03', 
            'password2': 'Testing@03', 
            'phone_number': '08012345678', 
            'subscription_plan': 'starter'
        }
        
        response = self.client.post(reverse('user:register'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

class LoginLogoutTestCase(APITestCase):
    '''Test case for log in and logout of a user'''
    
    # Create a set up function so what ever is inside is executed before the actual test cases
    def setUp(self):
        self.user = CustomUser.objects.create(
            email = 'test@gmail.com', 
            first_name= 'test', 
            last_name = 'tester', 
            password = 'Testing@03', 
            phone_number = '08012345678', 
            subscription_plan = 'starter',
            is_verified = True
        )
        
    def test_login(self):
        data = {
            'email': 'test@gmail.com',
            'password': 'Testing@03'
        }
        
        response = self.client.post(reverse('user:login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    # def test_logout(self):
    #     self.token = Token.objects.get(user__email='test@gmail.com').token
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
    #     response = self.client.post(reverse('user:logout'))
    #     # response.headers['Authorization'] = f'Bearer {self.token}'
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
