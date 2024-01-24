from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsVerifiedOrNoAccess(BasePermission):
    '''Permission class to prevent access by unverified users'''
    
    def has_object_permission(self, request, view, obj):
        return obj.is_verified
    