from rest_framework.permissions import BasePermission, SAFE_METHODS
from project.models import Project
from task.models import Task
from team.models import Team

from workspace.models import Member, Workspace

class IsWorkspaceOwnerOrEditorOrReadOnly(BasePermission):
    '''Permission to check if logged in user is a workspace creator or editor'''
    
    message = 'You are not authorized to make any changes to this workspace or its subsidiaries as you are not the creator or editor of this workspace.'
    
    def has_object_permission(self, request, view, obj):
        
        if request.method in SAFE_METHODS:
            return True
        else:
            workspace_obj = obj
            
            # Check if objects are of a certin object type to know what wworkspace object to work with
            if isinstance(obj, Workspace):
                workspace_obj = obj
            elif isinstance(obj, Project):
                workspace_obj = obj.workspace
            elif isinstance(obj, Task) or isinstance(obj, Team):
                workspace_obj = obj.project.workspace
            
            # get member based on current logged in user and workspace object
            member = Member.objects.filter(user=request.user, workspace=workspace_obj)
            
            # check if member exists in workspace
            if not member.exists():
                return False
            
            return (workspace_obj.creator == request.user) or member.first().role == 'editor'
        
        
class IsMemberOrReadOnly(BasePermission):     
    '''Permission to check if a user is a member of a workapce or it's subsidiaries (task, team, or project)'''
    
    message = 'Access denied as you are not a member of this workspace or its subsidiaries.'
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            # get member based on current logged in user
            member = Member.objects.get(user=request.user)
            
            # check if member is in project members
            return obj.members.contains(member)
