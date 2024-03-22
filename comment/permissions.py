from rest_framework.permissions import BasePermission, SAFE_METHODS

from workspace.models import Member

class IsProjectMemberComment(BasePermission):     
    '''Permission to check if a user is a member of a project. This is used for the comment model'''
    
    message = 'You are not a member of this project'
    
    def has_object_permission(self, request, view, obj):
        # get member based on current logged in user
        member = Member.objects.get(user=request.user)
        # check if member is in project members
        return obj.project.members.contains(member)
    
    
class IsProjectMemberCommentReply(BasePermission):     
    '''Permission to check if a user is a member of a project. This is used for the comment reply model'''
    
    message = 'You are not a member of this project'
    
    def has_object_permission(self, request, view, obj):
        # get member based on current logged in user
        member = Member.objects.get(user=request.user)
        # check if member is in project members
        return obj.comment.project.members.contains(member)