from rest_framework.permissions import BasePermission

class IsNotificationOwner(BasePermission):
    '''Permission to check if a notification is for the current logged in user'''
    
    message = 'Access denied as you are not the receiver of this notification'
    
    def has_object_permission(self, request, view, obj):
        return obj.receiver == request.user