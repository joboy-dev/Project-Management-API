from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from project.models import Project
from task.models import Task
from team.models import Team
from .permissions import IsTaskWorkspaceOwnerOrEditorOrReadOnly, IsTaskMemberOrReadOnly
from workspace.models import Member

from . import serializers

User = get_user_model()

class CreateGeneralProjectTaskView(generics.CreateAPIView):
    '''View to create general project task'''
    
    permission_classes = [IsAuthenticated, IsTaskWorkspaceOwnerOrEditorOrReadOnly]
    serializer_class = serializers.CreateGeneralProjectTaskSerializer
    queryset = Task.objects.all()
    
    
class CreateTeamTaskView(generics.CreateAPIView):
    '''View to create task-specific project task'''
    
    permission_classes = [IsAuthenticated, IsTaskWorkspaceOwnerOrEditorOrReadOnly]
    serializer_class = serializers.CreateTeamTaskSerializer
    queryset = Task.objects.all()


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''View to get, update and delete tasks'''
    
    permission_classes = [IsAuthenticated, IsTaskWorkspaceOwnerOrEditorOrReadOnly]
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
        team = Team.objects.get(id=self.kwargs['tem_id'])
        tasks = Task.objects.filter(team=team)
        
        return tasks
    
    def list(self, request, *args, **kwargs):
        team = Team.objects.get(id=self.kwargs['team_id'])
        taksa = Project.objects.filter(team=team)
        
        serializer = self.serializer_class(taksa, many=True)
        
        if taksa.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'There are no taksa in this team'}, status=status.HTTP_204_NO_CONTENT)
        