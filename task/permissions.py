from rest_framework.permissions import BasePermission, SAFE_METHODS

from workspace.models import Member

class IsTaskWorkspaceOwnerOrEditorOrReadOnly(BasePermission):
    '''Permission class to prevent unauthorized access to tasks'''
    
    message = 'You are not authorized to make any changes to this workspace as you are not the creator or an editor of the workspace.'
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            # get member based on current logged in user and workspace object
            member = Member.objects.filter(user=request.user, workspace=obj.project.workspace)
            
            # check if member exists in workspace
            if not member.exists():
                return False
            
            return (obj.project.workspace.creator == request.user) or member.first().role == 'editor'
        

class IsTaskMemberOrReadOnly(BasePermission):     
    '''Permission to check if a user is a member of a task'''
    
    message = 'You are not a member of this tean'
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            # get member based on current logged in user
            member = Member.objects.get(user=request.user)
            
            # check if member is in project members
            return obj.members.contains(member)