from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from project.models import Project
from team.models import Team
from team.permissions import IsTeamWorkspaceOwnerOrEditorOrReadOnly
from workspace.models import Member, Workspace

from . import serializers

User = get_user_model()

class CreateTeamView(generics.CreateAPIView):
    '''View to create team for a project'''
    
    permission_classes = [IsAuthenticated, IsTeamWorkspaceOwnerOrEditorOrReadOnly]
    serializer_class = serializers.CreateTeamSerializer
    queryset = Team.objects.all()
    

class TeamDetailsView(generics.RetrieveUpdateDestroyAPIView):
    '''View to get, update, and delete teams'''
    
    permission_classes = [IsAuthenticated, IsTeamWorkspaceOwnerOrEditorOrReadOnly]
    serializer_class = serializers.TeamDetailsSerializer

    def get(self, request, *args, **kwargs):
        try:
            team = Team.objects.get(id=self.kwargs['team_id'])
            serializer = self.serializer_class(team)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Team.DoesNotExist:
            return Response({'error': 'Team doe snot exist'}, status=status.HTTP_404_NOT_FOUND)
            
    def get_object(self):
        team = Team.objects.filter(id=self.kwargs['team_id'])
        self.check_object_permissions(self.request, obj=team)
        return team
    
    def delete(self, request, *args, **kwargs):
        try:
            super().delete(request, *args, **kwargs)
            return Response({'message': 'Team deleted'}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'error': 'Team does not exist'}, status=status.HTTP_404_NOT_FOUND)  
