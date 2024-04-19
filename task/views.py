from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from project.models import Project
from task.models import Task
from team.models import Team
from workspace.permissions import IsMemberOrReadOnly, IsWorkspaceOwnerOrEditorOrReadOnly
from workspace.models import Member

from . import serializers

User = get_user_model()

class CreateProjectTaskView(generics.CreateAPIView):
    '''View to create general project task'''
    
    permission_classes = [IsAuthenticated, IsWorkspaceOwnerOrEditorOrReadOnly]
    serializer_class = serializers.CreateProjectTaskSerializer
    queryset = Task.objects.all()
    
    
class CreateTeamTaskView(generics.CreateAPIView):
    '''View to create task-specific project task'''
    
    permission_classes = [IsAuthenticated, IsWorkspaceOwnerOrEditorOrReadOnly]
    serializer_class = serializers.CreateTeamTaskSerializer
    queryset = Task.objects.all()


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''View to get, update and delete tasks'''
    
    permission_classes = [IsAuthenticated, IsWorkspaceOwnerOrEditorOrReadOnly]
    serializer_class = serializers.TaskDetailSerializer
    
    def get(self, request, *args, **kwargs):
        try:
            task = Task.objects.get(id=self.kwargs['task_id'])
            serializer = self.serializer_class(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'error': 'Task doe snot exist'}, status=status.HTTP_404_NOT_FOUND)
            
    def get_object(self):
        task = Task.objects.get(id=self.kwargs['task_id'])
        self.check_object_permissions(self.request, obj=task)
        return task
    
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Task.DoesNotExist:
            return Response({'error': 'Task doe snot exist'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, *args, **kwargs):
        try:
            super().delete(request, *args, **kwargs)
            return Response({'message': 'Task deleted'}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'error': 'Task does not exist'}, status=status.HTTP_404_NOT_FOUND)  
        

class GetTasksForTeamView(generics.ListAPIView):
    '''View to get tasks for a specific team'''
    
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.TaskDetailSerializer
    
    def get_queryset(self):
        team = Team.objects.get(id=self.kwargs['team_id'])
        tasks = Task.objects.filter(team=team)
        
        return tasks
    
    def list(self, request, *args, **kwargs):
        team = Team.objects.get(id=self.kwargs['team_id'])
        tasks = Task.objects.filter(team=team)
        
        serializer = self.serializer_class(tasks, many=True)
        
        if tasks.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'There are no tasks for this team'}, status=status.HTTP_204_NO_CONTENT)
        
        
class GetProjectTasksView(generics.ListAPIView):
    '''View to get tasks for a project'''
    
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.TaskDetailSerializer
    
    def get_queryset(self):
        project = Project.objects.get(id=self.kwargs['project_id'])
        tasks = Task.objects.filter(project=project)
        
        return tasks
    
    def list(self, request, *args, **kwargs):
        project = Project.objects.get(id=self.kwargs['project_id'])
        tasks = Task.objects.filter(project=project)
        
        serializer = self.serializer_class(tasks, many=True)
        
        if tasks.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'There are no tasks for this project'}, status=status.HTTP_204_NO_CONTENT)
        
        
class AddMemberToTaskView(APIView):
    '''View to add a member to a task'''
    
    permission_classes = [IsAuthenticated, IsWorkspaceOwnerOrEditorOrReadOnly]
    
    def post(self, request, task_id, member_id):
        task = Task.objects.get(id=self.kwargs['task_id'])
        members = Member.objects.filter(id=self.kwargs['member_id'], workspace=task.project.workspace)
        self.check_object_permissions(request, obj=task)
        member = members.first()
        
        if not members.exists():
            return Response({'error': 'Member does not exist in this workspace'}, status=status.HTTP_404_NOT_FOUND)
            
        try:
            if task.members.contains(member):
                return Response({'error': 'This member already exists in this task'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                task.members.add(member)
                task.save()
                return Response({'message': f'Member {member.user.email} added to task'}, status=status.HTTP_404_NOT_FOUND)
                
        except Member.DoesNotExist:
            return Response({'error': 'Member does not exist in this task'}, status=status.HTTP_404_NOT_FOUND)
            
        except Task.DoesNotExist:
            return Response({'error': 'Task does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    
class RemoveMemberFromTaskView(APIView):
    '''View to remive a member from a task'''
    
    permission_classes = [IsAuthenticated, IsWorkspaceOwnerOrEditorOrReadOnly]
    
    def post(self, request, task_id, member_id):
        task = Task.objects.get(id=self.kwargs['task_id'])
        members = Member.objects.filter(id=self.kwargs['member_id'], workspace=task.project.workspace)
        self.check_object_permissions(request, obj=task)
        member = members.first()
        
        if not members.exists():
            return Response({'error': 'Member does not exist in this workspace'}, status=status.HTTP_404_NOT_FOUND)
            
        try:
            if not task.members.contains(member):
                return Response({'error': 'Member is not a part of the task'})
            
            task.members.remove(member)
            task.save()
            
            return Response({'message': f'Member {member.user.email} removed from task'})
            
        except Member.DoesNotExist:
            return Response({'error': 'Member does not exist in this task'}, status=status.HTTP_404_NOT_FOUND)
            
        except Task.DoesNotExist:
            return Response({'error': 'Task does not exist'}, status=status.HTTP_404_NOT_FOUND)
        

class ToggleCompletionStatusView(APIView):
    '''View to mark a task as complete'''
    
    permission_classes = [IsAuthenticated, IsWorkspaceOwnerOrEditorOrReadOnly]
    
    def post(self, request, task_id):
        task = Task.objects.get(id=self.kwargs['task_id'])
        self.check_object_permissions(request, obj=task)
        
        try:
            task.is_complete = not task.is_complete
            task.save()
            
            status_message = 'complete' if task.is_complete else 'incomplete'
            
            return Response({'message': f'Task marked as {status_message}'}, status=status.HTTP_200_OK)
        
        except Task.DoesNotExist:
            return Response({'error': 'Task does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
        