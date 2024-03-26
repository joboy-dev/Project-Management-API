from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from comment.models import Comment, CommentReply
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
    
    serializer_class = serializers.CommentDetailsSerializer
    permission_classes = [IsAuthenticated, IsProjectMemberComment]
    
    def get(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=self.kwargs['comment_id'])
            serializer = self.serializer_class(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    def get_object(self):
        comment = Comment.objects.get(id=self.kwargs['comment_id'])
        self.check_object_permissions(self.request, comment)
        return comment
    
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, *args, **kwargs):
        try:
            super().delete(request, *args, **kwargs)
            return Response({'message': 'Comment deleted'}, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        
class GetAllCommentsView(generics.ListAPIView):
    '''View to get all comments for a project'''
    
    serializer_class = serializers.CommentDetailsSerializer
    
    def get_queryset(self):
        project = Project.objects.get(id=self.kwargs['project_id'])
        comments = Comment.objects.filter(project=project)
        return comments
    
    def list(self, request, *args, **kwargs):
        project = Project.objects.get(id=self.kwargs['project_id'])
        comments = Comment.objects.filter(project=project)
        
        serializer = self.serializer_class(comments, many=True)
        
        if comments.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'There are no comments for this project'}, status=status.HTTP_204_NO_CONTENT)
            

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
    
    serializer_class = serializers.CommentReplyDetailsSerializer
    permission_classes = [IsAuthenticated, IsProjectMemberCommentReply]
    
    def get(self, request, *args, **kwargs):
        try:
            reply = CommentReply.objects.get(id=self.kwargs['comment_reply_id'])
            serializer = self.serializer_class(reply)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment reply does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    def get_object(self):
        reply = CommentReply.objects.get(id=self.kwargs['comment_reply_id'])
        self.check_object_permissions(self.request, reply)
        return reply
    
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except CommentReply.DoesNotExist:
            return Response({'error': 'Comment reply does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, *args, **kwargs):
        try:
            super().delete(request, *args, **kwargs)
            return Response({'message': 'Comment reply deleted'}, status=status.HTTP_200_OK)
        except CommentReply.DoesNotExist:
            return Response({'error': 'Comment reply does not exist'}, status=status.HTTP_404_NOT_FOUND)
    

class GetAllCommentRepliesView(generics.ListAPIView):
    '''View to get all comment replies'''
    
    serializer_class = serializers.CommentDetailsSerializer
    
    def get_queryset(self):
        comment = Comment.objects.get(id=self.kwargs['comment_id'])
        replies = CommentReply.objects.filter(comment=comment)
        return replies
    
    def list(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=self.kwargs['comment_id'])
        replies = CommentReply.objects.filter(comment=comment)
        
        serializer = self.serializer_class(replies, many=True)
        
        if replies.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'There are no replies for this comment'}, status=status.HTTP_204_NO_CONTENT)