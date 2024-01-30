from rest_framework.permissions import BasePermission, SAFE_METHODS

from workspace.models import Member

class IsTeamWorkspaceOwnerOrEditorOrReadOnly(BasePermission):
    '''Permission class to cheeck if the workspace project the team is under is accessible to a user.'''
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return False
        else:
            # get member based on current logged in user and workspace object
            member = Member.objects.filter(user=request.user, workspace=obj.project.workspace)
            
            # check if member exists in workspace
            if member.count() == 0:
                return False
            
            return (obj.project.workspace.creator == request.user) or member.first().role == 'editor'