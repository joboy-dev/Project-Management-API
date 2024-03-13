from django.contrib.auth import get_user_model
from rest_framework import serializers

from datetime import datetime
from project.models import Project
from workspace.models import Member, Workspace
from workspace.serializers import MemberSerializer

User = get_user_model()

class ProjectSerializer(serializers.ModelSerializer):
    '''Serializer to create a new project'''
    
    workspace = serializers.StringRelatedField(read_only=True)
    members = MemberSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['id', 'workspace', 'members', 'created_by', 'is_complete']
        
    def validate(self, data):
        # Remove timezone
        now = datetime.now().replace(tzinfo=None)
        data['start_date'] = data['start_date'].replace(tzinfo=None)
        data['end_date'] = data['end_date'].replace(tzinfo=None)
        
        if ((data['start_date']) < now) or (data['end_date'] < now):
            raise serializers.ValidationError({'error': 'Date cannot be in the past'})
        
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError({'error': 'Start date cannot be greater than end date'})
        
        workspace_id = self.context['view'].kwargs['workspace_id']
        workspace = Workspace.objects.get(id=workspace_id)
        
        # filter member object so that members from outside the workspace cannot be added
        member = Member.objects.filter(user=self.context['request'].user, workspace=workspace)
       
        # check if user belongs in workspace
        if not member.exists():
            raise serializers.ValidationError({'error': 'You do not exist in this workspace'})
        
        # check if member is an editor
        if member.first().role != 'editor':
            raise serializers.ValidationError({'error': 'You are not an editor in the workspace'})
        
        return data
    
    def create(self, validated_data):
        name = validated_data.get('name')
        description = validated_data.get('description')
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')
        label_color = validated_data.get('label_color')
        
        workspace_id = self.context['view'].kwargs['workspace_id']
        workspace = Workspace.objects.get(id=workspace_id)
        
        # filter member object so that members from outside the workspace cannot be added
        member = Member.objects.filter(user=self.context['request'].user, workspace=workspace)
        
        project = Project.objects.create(
            name=name,
            description=description,
            label_color=label_color,
            is_complete=False,
            start_date=start_date,
            end_date=end_date,
            workspace=workspace,
            created_by=member.first()
        )
        
        # add member to members list in project
        project.members.set(member)
        project.save()
        
        return project
    
    
class ProjectDetailsSerializer(serializers.ModelSerializer):
    '''Serializer to create a new project'''
    
    workspace = serializers.StringRelatedField(read_only=True)
    members = MemberSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['id', 'workspace', 'members', 'created_by', 'is_complete']
        
    def validate(self, data):
        # Remove timezone
        now = datetime.now().replace(tzinfo=None)
        
        if data.get('start_date'):
            data['start_date'] = data['start_date'].replace(tzinfo=None)
            if data['start_date'] < now:
                raise serializers.ValidationError({'error': 'Date cannot be in the past'})
            
        if data.get('end_date'):
            data['end_date'] = data['end_date'].replace(tzinfo=None)
            if data['end_date'] < now:
                raise serializers.ValidationError({'error': 'Date cannot be in the past'})
        
        return data
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
            
        instance.save()
        return instance
          