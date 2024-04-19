from rest_framework import serializers

from comment.models import Comment, CommentReply
from project.models import Project
from workspace.models import Member
from workspace.serializers import MemberSerializer

class CommentSerializer(serializers.ModelSerializer):
    '''Serializer for comments'''
    
    commenter = MemberSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'project', 'commenter']
    
    def create(self, validated_data):
        project = Project.objects.get(id=self.context['view'].kwargs['project_id'])
        member = Member.objects.get(user=self.context['request'].user, workspace=project.workspace)
        # Create comment
        comment = Comment.objects.create(
            comment=validated_data.get('comment'),
            project=project,
            commenter=member
        )
        
        return comment
 
 
class CommentDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for comment details'''
    
    commenter = MemberSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'project', 'commenter']
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
            
        instance.save()
        return instance
    

class CommentReplySerializer(serializers.ModelSerializer):
    '''Serializer for comment replies'''
    
    commenter = MemberSerializer(read_only=True)
    
    class Meta:
        model = CommentReply
        fields = '__all__'
        read_only_fields = ['id', 'comment', 'commenter']
    
    def create(self, validated_data):
        comment = Comment.objects.get(id=self.context['view'].kwargs['comment_id'])
        member = Member.objects.get(user=self.context['request'].user, workspace=comment.project.workspace)
        
        try:
            # Create comment
            reply = CommentReply.objects.create(
                reply=validated_data.get('reply'),
                comment=comment,
                commenter=member
            )
        except Member.DoesNotExist:
            raise serializers.ValidationError('Member does not exist in this workspace')
        
        return reply
 
 
class CommentReplyDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for comment reply details'''
    
    commenter = MemberSerializer(read_only=True)
    
    class Meta:
        model = CommentReply
        fields = '__all__'
        read_only_fields = ['id', 'comment', 'commenter']
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
            
        instance.save()
        return instance
    

