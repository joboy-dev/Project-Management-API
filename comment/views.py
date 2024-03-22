from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from project.models import Project
from workspace.models import Member, Workspace
from .permissions import IsProjectMemberComment, IsProjectMemberCommentReply

from . import serializers

User = get_user_model()

class CreateCommentView(generics.CreateAPIView):
    '''View to create a comment'''
    
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectMemberComment]
    
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CommentDetailsView(generics.RetrieveUpdateDestroyAPIView):
    '''View to get, update and delete a comment'''
    

class GetAllCommentsView(generics.ListAPIView):
    '''View to get all comments'''
    

class CreateCommentReplyView(generics.CreateAPIView):
    '''View to create reply to a comment'''
    
    serializer_class = serializers.CommentReplySerializer
    permission_classes = [IsAuthenticated, IsProjectMemberCommentReply]
    
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CommentReplyDetailsView(generics.RetrieveUpdateDestroyAPIView):
    '''View to get, update and delete a comment reply'''
    

class GetAllCommentRepliesView(generics.ListAPIView):
    '''View to get all comment replies'''