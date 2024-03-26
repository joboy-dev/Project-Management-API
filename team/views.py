from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from project.models import Project
from team.models import Team
from team.permissions import IsTeamWorkspaceOwnerOrEditorOrReadOnly, IsTeamMemberOrReadOnly
from workspace.models import Member
from workspace.permissions import IsMemberOrReadOnly

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
        team = Team.objects.get(id=self.kwargs['team_id'])
        self.check_object_permissions(self.request, obj=team)
        return team
    
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Team.DoesNotExist:
            return Response({'error': 'Team does not exist'}, status=status.HTTP_404_NOT_FOUND)  
        
    def delete(self, request, *args, **kwargs):
        try:
            super().delete(request, *args, **kwargs)
            return Response({'message': 'Team deleted'}, status=status.HTTP_200_OK)
        except Team.DoesNotExist:
            return Response({'error': 'Team does not exist'}, status=status.HTTP_404_NOT_FOUND)  
        
        
class AddMemberToTeamView(APIView):
    '''View to add a member to a team'''
    
    permission_classes = [IsAuthenticated, IsTeamWorkspaceOwnerOrEditorOrReadOnly]
    
    def post(self, request, team_id, member_id):
        team = Team.objects.get(id=self.kwargs['team_id'])
        members = Member.objects.filter(id=self.kwargs['member_id'], workspace=team.project.workspace)
        self.check_object_permissions(request, obj=team)
        
        if not members.exists():
            return Response({'error': 'This member does not exist in this workspace'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if team.members.contains(members.first()):
                return Response({'error': 'This member is already in the team'}, status=status.HTTP_400_BAD_REQUEST)
        
            team.members.add(members.first())
            team.save()
            
            return Response({'message': f'Member {members.first().user.email} added to team'})
        
        except Member.DoesNotExist:
            return Response({'error': 'Member does not exist in this team'}, status=status.HTTP_404_NOT_FOUND)
            
        except Team.DoesNotExist:
            return Response({'error': 'Team does not exist'}, status=status.HTTP_404_NOT_FOUND)
           

class RemoveMemberFromTeamView(APIView):
    '''View to remove a member from a team'''
    
    permission_classes = [IsAuthenticated, IsTeamWorkspaceOwnerOrEditorOrReadOnly]
    
    def post(self, request, team_id, member_id):
        team = Team.objects.get(id=self.kwargs['team_id'])
        members = Member.objects.filter(id=self.kwargs['member_id'], workspace=team.project.workspace)
        self.check_object_permissions(request, obj=team)
        
        if not members.exists():
            return Response({'error': 'This member does not exist in this workspace'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if not team.members.contains(members.first()):
                return Response({'error': 'This member is not in the team'}, status=status.HTTP_400_BAD_REQUEST)
        
            team.members.remove(members.first())
            team.save()
            
            return Response({'message': f'Member {members.first().user.email} removed from team'})
        
        except Member.DoesNotExist:
            return Response({'error': 'Member does not exist in this team'}, status=status.HTTP_404_NOT_FOUND)
            
        except Team.DoesNotExist:
            return Response({'error': 'Team does not exist'}, status=status.HTTP_404_NOT_FOUND)
           

class GetAllProjectTeams(generics.ListAPIView):
    '''View to get all teams in a specific project'''
    
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.TeamDetailsSerializer
    
    def get_queryset(self):
        project = Project.objects.get(id=self.kwargs['project_id'])
        teams = Team.objects.filter(project=project)
        return teams
    
    def list(self, request, *args, **kwargs):
        project = Project.objects.get(id=self.kwargs['project_id'])
        teams = Team.objects.filter(project=project)
        serializer = self.serializer_class(teams, many=True)
        
        if teams.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'There are no teams in this project'}, status=status.HTTP_204_NO_CONTENT)
        