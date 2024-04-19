from rest_framework.permissions import BasePermission, SAFE_METHODS

from comment.models import CommentReply
from workspace.models import Member

class IsProjectMemberComment(BasePermission):     
    '''Permission to check if a user is a member of a project'''
    
    message = 'You are not a member of this project'
    
    def has_object_permission(self, request, view, obj):
        # check if member is in project members
        comment_obj = obj
        if isinstance(obj, CommentReply):
            comment_obj = obj.comment
            
        # get member based on current logged in user
        member = Member.objects.get(user=request.user, workspace=comment_obj.project.workspace)
        
        return comment_obj.project.members.contains(member)
    

class IsCommentOwner(BasePermission):
    '''Permission to check if the current logged in user is the owner of the comment'''
    
    message = 'You are not the owner of this comment so you cannot make changes to it.'
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return request.user == obj.commenter.user