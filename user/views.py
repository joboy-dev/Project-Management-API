import smtplib
import os
from dotenv import load_dotenv
from pathlib import Path

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase
import jwt

from . import serializers
from project_management_api import permissions
from .util import Util

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))

User = get_user_model()

def send_verification_email(request, email):
    '''Function to send verification email'''
    
    user = User.objects.get(email=email)
    token = RefreshToken.for_user(user).access_token
    
    current_site = get_current_site(request)
    relative_link = reverse('user:verify-email')
    absolute_url = f'http://{current_site}{relative_link}?token={token}'
    
    data = {
        'subject': 'Verify your email address',
        'body': f'Hi, {user.first_name}.\n\nClick the link below to verify your email address:\n{absolute_url}\n\nThe link expires after 5-15 minutes.',
        'email': user.email
    }
    
    Util.send_email(data)
    
    
class RegisterView(generics.GenericAPIView):
    '''View to register users'''

    serializer_class = serializers.CreateAccountSerializer
    parser_classes = [MultiPartParser]
    queryset = User.objects.all()
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        try:
            send_verification_email(request, email=serializer.data['email'])
        except Exception as e:
            return Response({
                'exception': f'{e}',
                'error': 'An error occured. Try again later',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'user': serializer.data,
            'message': f"Account created successfully. Check {serializer.data['email']} for a verification link"},
            status=status.HTTP_201_CREATED
        )
 
        
class VerifyEmailView(generics.GenericAPIView):
    '''View to verify email address'''
    
    def get(self, request):
        # get token from url parameters
        token = request.GET['token']
        
        try:
            # decode token
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            # get user based on user_id from payload
            user = User.objects.get(id=payload['user_id'])
                        
            if user.is_verified:
                return Response({'error': 'You have been verified already'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if user is not None:
                    user.is_verified = True
                    user.save()
                    return Response({'message': 'Your email has been verified successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'This user does not exist'}, status=status.HTTP_400_BAD_REQUEST)
                    
        except jwt.ExpiredSignatureError:
            return Response({'error': 'This verification link is expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'exception': f'{e}',
                'error': 'An error occured. Try again later',
            }, status=status.HTTP_400_BAD_REQUEST)
            

class ResendVerificationEmailView(generics.GenericAPIView):
    '''View to resend verification email'''
    
    serializer_class = serializers.ResendEmailVerificationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = User.objects.get(email=serializer.data['email'])
            if user.is_verified:
                return Response({'error': 'You have been verified already'}, status=status.HTTP_400_BAD_REQUEST)
            
            send_verification_email(request, email=serializer.data['email'])
            
        except Exception as e:
            return Response({
                'exception': f'{e}',
                'error': 'An error occured. Try again later',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'message': f"Verification email sent successfully. Check {serializer.data['email']} for a new verification link"},
            status=status.HTTP_201_CREATED
        )
    

class LoginView(generics.GenericAPIView):
    '''View to login users'''
    
    serializer_class = serializers.LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
        

class UserDetailsView(generics.RetrieveUpdateAPIView):
    '''View to get, and update user account'''
    
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserDetailsSerializer
    
    def get_object(self):
        return self.request.user
    

class ChangeEmailView(generics.UpdateAPIView):
    ''' View to change user email address'''
    
    serializer_class = serializers.ChangeEmailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            super().update(request, *args, **kwargs)
            # send email verification to new email
            send_verification_email(self.request, email=serializer.data['email'])
            
            # Get user details
            user = User.objects.get(id=self.request.user.id)
            print(user.email)
            
            # Make user unverifed because of change in email
            user.is_verified = False
            user.save()            
            
        except Exception as e:
            return Response({
                'exception': f'{e}',
                'error': 'An error occured. Try again later',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'message': f"Email changed successfully. Check {serializer.data['email']} for a new email verification link"},
            status=status.HTTP_201_CREATED
        )

    

class ChangePasswordView(generics.UpdateAPIView):
    '''View to change user password'''

    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    ''' View to logout users'''
    
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.LogoutSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        

class RefreshTokenView(TokenViewBase):
    '''View to refresh token'''
    
    serializer_class = serializers.RefreshAccessSerializer