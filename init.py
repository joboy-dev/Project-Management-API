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
import jwt