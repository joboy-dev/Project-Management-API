from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from project.models import Project
from workspace.models import Member, Workspace
from .permissions import IsProjectWorkspaceOwnerOrReadOnly, IsProjectMemberOrReadOnly
from workspace.permissions import IsMemberOrReadOnly

from . import serializers

User = get_user_model()

class CreateProjectView(generics.CreateAPIView):
    '''View to list and create projects'''
    
    serializer_class = serializers.ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectWorkspaceOwnerOrReadOnly]
    queryset = Project.objects.all()
    
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ProjectDetailsView(generics.RetrieveUpdateDestroyAPIView):
    '''View to get, update, and delete project'''
    
    serializer_class = serializers.ProjectDetailsSerializer
    permission_classes = [IsAuthenticated, IsProjectWorkspaceOwnerOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(id=self.kwargs['project_id'])
            serializer = self.serializer_class(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'error': 'Project does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    def get_object(self):
        project = Project.objects.get(id=self.kwargs['project_id'])
        self.check_object_permissions(self.request, obj=project)
        return project
    
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Project.DoesNotExist:
            return Response({'error': 'Project does not exist'}, status=status.HTTP_404_NOT_FOUND)  
    
    def delete(self, request, *args, **kwargs):
        try:
            super().delete(request, *args, **kwargs)
            return Response({'message': 'Project deleted'}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'error': 'Project does not exist'}, status=status.HTTP_404_NOT_FOUND)  
        

class AddMemberToProjectView(generics.GenericAPIView):
    '''View to add a member to a project'''
    
    permission_classes = [IsAuthenticated, IsProjectWorkspaceOwnerOrReadOnly]
    
    def post(self, request, project_id, member_id):
        project = Project.objects.get(id=self.kwargs['project_id'])
        members = Member.objects.filter(id=self.kwargs['member_id'], workspace=project.workspace)
        self.check_object_permissions(request, obj=project)
        member = members.first()
        
        if not members.exists():
            return Response({'error': 'Member does not exist in this workspace'}, status=status.HTTP_404_NOT_FOUND)
        
        # if member.user == request.user:
        #     return Response({'error': 'You cannot add yourself to a project'}, status=status.HTTP_404_NOT_FOUND)
            
        try:
            if project.members.contains(member):
                return Response({'error': 'This member already exists in this project'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                project.members.add(member)
                project.save()
                return Response({'message': f'Member {member.user.email} added to project'}, status=status.HTTP_404_NOT_FOUND)
                
        except Member.DoesNotExist:
            return Response({'error': 'Member does not exist in this project'}, status=status.HTTP_404_NOT_FOUND)
            
        except Project.DoesNotExist:
            return Response({'error': 'Project does not exist'}, status=status.HTTP_404_NOT_FOUND)
        

class RemoveMemberFromProjectView(generics.GenericAPIView):
    '''View to remove a member from a project'''
    
    permission_classes = [IsAuthenticated, IsProjectWorkspaceOwnerOrReadOnly]
    
    def post(self, request, project_id, member_id):
        project = Project.objects.get(id=self.kwargs['project_id'])
        members = Member.objects.filter(id=self.kwargs['member_id'], workspace=project.workspace)
        self.check_object_permissions(request, obj=project)
        
        member = members.first()
        
        if members.count() == 0:
            return Response({'error': 'Member does not exist in this workspace'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            if not project.members.contains(member):
                return Response({'error': 'This member does not exist in this project'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                project.members.remove(member)
                project.save()
                return Response({'message': f'Member {member.user.email} removed from project'}, status=status.HTTP_404_NOT_FOUND)
        except Member.DoesNotExist:
            return Response({'error': 'Member does not exist in this project'}, status=status.HTTP_404_NOT_FOUND)
            
        except Project.DoesNotExist:
            return Response({'error': 'Project does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
        
class GetProjectsInWorkspaceView(generics.ListAPIView):
    '''View to get all projects in a workspace'''
    
    serializer_class = serializers.ProjectDetailsSerializer
    
    def get_queryset(self):
        workspace = Workspace.objects.get(id=self.kwargs['workspace_id'])
        projects = Project.objects.filter(workspace=workspace)
        
        return projects
    
    def list(self, request, *args, **kwargs):
        workspace = Workspace.objects.get(id=self.kwargs['workspace_id'])
        projects = Project.objects.filter(workspace=workspace)
        
        serializer = self.serializer_class(projects, many=True)
        
        if projects.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'There are no projects in this workspace'}, status=status.HTTP_204_NO_CONTENT)
        

class MarkProjectAsCompleteView(generics.GenericAPIView):
    '''View to mark a project as complete'''
    
    permission_classes = [IsAuthenticated, IsProjectWorkspaceOwnerOrReadOnly, IsMemberOrReadOnly]
    
    def post(self, request, project_id):
        project = Project.objects.get(id=self.kwargs['project_id'])
        member = Member.objects.get(user=request.user)
        self.check_object_permissions(request, obj=project)
        
        try:
            project.is_complete = True
            project.save()      
            return Response({'message': 'Project marked as complete'}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'error': 'Project does not exist'}, status=status.HTTP_404_NOT_FOUND)
            