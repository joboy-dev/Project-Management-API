from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsTaskWorkspaceOwnerOrEditorOrReadOnly(BasePermission):
    '''Permission class to prevent unauthorized access to tasks'''
    
    