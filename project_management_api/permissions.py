from rest_framework.permissions import BasePermission

class IsActiveOrNoAccess(BasePermission):
    '''Permission class to prevent access by inactive users i.e. users with deleted accounts.'''
    
    message = 'Your account is inactive.'
    
    def has_permission(self, request, view):
        return request.user.is_active
    

class IsVerifiedOrNoAccess(BasePermission):
    '''Permission class to prevent access by unverified users'''
    
    message = 'Your email has not been verified. Verify your email to continue.'
    
    def has_permission(self, request, view):
        return request.user.is_verified
    