from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from project_management_api.permissions import IsVerifiedOrNoAccess
from workspace.models import Member, Workspace
from workspace.permissions import IsWorkspaceOwnerOrEditorOrReadOnly

from . import serializers

User = get_user_model()

class CreateWorkspaceView(generics.CreateAPIView):
    '''View to create workspace'''
    
    permission_classes = [IsAuthenticated, IsVerifiedOrNoAccess]
    serializer_class = serializers.CreateWorkspaceSerializer
    
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class WorkspaceDetailsView(generics.RetrieveUpdateDestroyAPIView):
    '''View to get, update and delete workspace details'''
    
    permission_classes = [IsAuthenticated, IsVerifiedOrNoAccess, IsWorkspaceOwnerOrEditorOrReadOnly]
    serializer_class = serializers.WorkspaceDetailsSerializer
    
    def get(self, request, *args, **kwargs):        
        try:
            workspace = Workspace.objects.get(id=self.kwargs['workspace_id'])
            serializer = self.serializer_class(workspace)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Workspace.DoesNotExist:
            return Response({'error': 'Workspace does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    def get_object(self):
        workspace = Workspace.objects.get(id=self.kwargs['workspace_id'])
        self.check_object_permissions(self.request, workspace)
        return workspace
    
    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Workspace.DoesNotExist:
            return Response({'error': 'Workspace does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, *args, **kwargs):
        try:
            super().delete(request, *args, **kwargs)
            return Response({'message': 'Workspace deleted'}, status=status.HTTP_200_OK)
        except Workspace.DoesNotExist:
            return Response({'error': 'Workspace does not exist'}, status=status.HTTP_404_NOT_FOUND)    
    
    
class AddMemberToWorkspaceView(generics.CreateAPIView):
    '''View to add a member to workspace'''
    
    permission_classes = [IsAuthenticated, IsVerifiedOrNoAccess, IsWorkspaceOwnerOrEditorOrReadOnly]
    serializer_class = serializers.MemberSerializer
    
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        
        workspace = Workspace.objects.get(id=self.kwargs['workspace_id'])
        # Check permission class
        self.check_object_permissions(self.request, workspace)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class RemoveMemberFromWorkspaceView(generics.GenericAPIView):
    '''View to remove member from workspace'''
    
    permission_classes = [IsAuthenticated, IsVerifiedOrNoAccess, IsWorkspaceOwnerOrEditorOrReadOnly]
    serializer_class = serializers.MemberSerializer
    
    def post(self, request, workspace_id, user_id):
        workspace_id = self.kwargs['workspace_id']
        user_id = self.kwargs['user_id']
        
        workspace = Workspace.objects.get(id=workspace_id)
        user = User.objects.get(id=user_id)
        
        self.check_object_permissions(request, obj=workspace)
        
        if user == request.user:
            return Response({'error': 'You cannot remove yourself from the workspace'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # get member to delete based on the workspace and user objects
                member = Member.objects.get(workspace=workspace, user=user)
                member.delete()
                
                workspace.current_no_of_members -= 1
                workspace.save()
                
                return Response({'message': f'Member {member.user.email} has been removed'})
            
            except Member.DoesNotExist:
                return Response({'error': 'Member does not exist in workspace'}, status=status.HTTP_404_NOT_FOUND)
            

class GetWorkspaceMembersView(generics.ListAPIView):
    '''View to view all workspace members'''
    
    permission_classes = [IsAuthenticated, IsVerifiedOrNoAccess, IsWorkspaceOwnerOrEditorOrReadOnly]
    serializer_class = serializers.MemberSerializer
    
    def get_queryset(self):
        workspace_id = self.kwargs['workspace_id']
        workspace = Workspace.objects.get(id=workspace_id)
        
        members = Member.objects.filter(workspace=workspace)
        return members
    
    def list(self, request, *args, **kwargs):
        workspace_id = self.kwargs['workspace_id']
        workspace = Workspace.objects.get(id=workspace_id)
        
        members = Member.objects.filter(workspace=workspace)
        serializer = self.serializer_class(members, many=True)
        
        if members.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'There are no members in this workspace'}, status=status.HTTP_204_NO_CONTENT)
        
    
class UpdateMemberRoleView(generics.UpdateAPIView):
    '''View to update workspace member role'''
    
    permission_classes = [IsAuthenticated, IsVerifiedOrNoAccess, IsWorkspaceOwnerOrEditorOrReadOnly]
    serializer_class = serializers.UpdateMemberSerializer
    
    def get_object(self):
        user = User.objects.get(id=self.kwargs['user_id'])
        workspace = Workspace.objects.get(id=self.kwargs['workspace_id'])
        
        member = Member.objects.get(user=user, workspace=workspace)
        
        self.check_object_permissions(self.request, obj=workspace)
        return member
        
    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    