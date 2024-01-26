from rest_framework.permissions import BasePermission, SAFE_METHODS

from workspace.models import Member

class IsWorkspaceOwnerOrEditorOrReadOnly(BasePermission):
    '''Permission to check against unverified workspaces'''
    
    message = 'You are not authorized to make any changes to this workspace as you are not the creator or an editor.'
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            member = Member.objects.get(user=request.user)
            return (obj.creator == request.user)
        
