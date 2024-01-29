from rest_framework.permissions import BasePermission, SAFE_METHODS

from workspace.models import Member

class IsProjectWorkspaceOwnerOrReadOnly(BasePermission):
    '''Permission to check against unverified workspaces'''
    
    message = 'You are not authorized to make any changes to this workspace as you are not the creator or an editor of the workspace.'
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            # get member based on current logged in user and workspace object
            member = Member.objects.filter(user=request.user, workspace=obj.workspace)
            
            # check if member exists in workspace
            if member.count() == 0:
                return False
            
            return (obj.workspace.creator == request.user) or member.first().role == 'editor'        
