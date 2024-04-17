from rest_framework import serializers
from datetime import datetime
from project.models import Project

from task.models import Task
from team.models import Team
from workspace.models import Member
from workspace.serializers import MemberSerializer

class CreateProjectTaskSerializer(serializers.ModelSerializer):
    '''Serializer to create a non-team task'''
    
    members = MemberSerializer(read_only=True, many=True)
    created_by = serializers.SerializerMethodField(read_only=True)
    
    def get_created_by(self, obj):
        return obj.id
        
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'project', 'members', 'created_by', 'is_complete', 'is_team_task', 'team']
        
    def validate(self, data):
        # Remove timezone
        now = datetime.now().replace(tzinfo=None)
        data['start_date'] = data['start_date'].replace(tzinfo=None)
        data['end_date'] = data['end_date'].replace(tzinfo=None)
        
        # date time validation
        if ((data['start_date']) < now) or (data['end_date'] < now):
            raise serializers.ValidationError({'error': 'Date cannot be in the past'})
        
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError({'error': 'Start date cannot be greater than end date'})
        
        project = Project.objects.get(id=self.context['view'].kwargs['project_id'])
        # get member based on logged in user and project workspace to avoid another user creating a task in a project that is not in their workspace
        member = Member.objects.filter(user=self.context['request'].user, workspace=project.workspace)
        
        if not member.exists():
            raise serializers.ValidationError({'error': 'You do not exist in the workspace'})
        
        if member.first().role != 'editor':
            raise serializers.ValidationError({'error': 'You are not an editor in the workspace'})
        
        # Check if task start or end date is past project start or end date
        if data['start_date'] > project.end_date.replace(tzinfo=None) or data['end_date'] > project.end_date.replace(tzinfo=None):
            raise serializers.ValidationError({'error': 'Task start or end dates must not be after project end date'})
            
        return data
    
    def create(self, validated_data):
        name = validated_data.get('name')
        description = validated_data.get('description')
        label_color = validated_data.get('label_color')
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')        
        project = Project.objects.get(id=self.context['view'].kwargs['project_id'])
        
        # filter member object so that members from outside the workspace cannot be added
        member = Member.objects.filter(user=self.context['request'].user, workspace=project.workspace)
        
        task = Task.objects.create(
            name=name,
            description=description,
            label_color=label_color,
            is_complete=False,
            is_team_task=False,
            start_date=start_date,
            end_date=end_date,
            project=project,
            created_by=member.first()
        )
        
        # add member to members list in task
        task.members.set(member)
        task.save()
        
        return task
    
class CreateTeamTaskSerializer(serializers.ModelSerializer):
    '''Serializer to create a team task'''
    
    members = MemberSerializer(read_only=True, many=True)
    created_by = serializers.SerializerMethodField(read_only=True)
    
    def get_created_by(self, obj):
        return obj.id
    
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'project', 'members', 'created_by', 'is_complete', 'is_team_task', 'team']
        
    def validate(self, data):
        # Remove timezone
        now = datetime.now().replace(tzinfo=None)
        data['start_date'] = data['start_date'].replace(tzinfo=None)
        data['end_date'] = data['end_date'].replace(tzinfo=None)
        
        # date time validation
        if ((data['start_date']) < now) or (data['end_date'] < now):
            raise serializers.ValidationError({'error': 'Date cannot be in the past'})
        
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError({'error': 'Start date cannot be greater than end date'})
        
        project = Project.objects.get(id=self.context['view'].kwargs['project_id'])
        team = Team.objects.get(id=self.context['view'].kwargs['team_id'])
        # get member based on logged in user and project workspace
        member = Member.objects.filter(user=self.context['request'].user, workspace=project.workspace)
        
        if not member.exists():
            raise serializers.ValidationError({'error': 'You do not exist in the workspace'})
        
        if member.first().role != 'editor':
            raise serializers.ValidationError({'error': 'You are not an editor in the workspace'})
        
        # check if project is linked with the team
        if team.project != project:
            raise serializers.ValidationError({'error': 'This team does not exist for the project'})
        
        # check if logged in member is part of the team
        if not team.members.contains(member.first()):
            raise serializers.ValidationError({'error': 'You do not belong in this team'})
        
        # Check if task start or end date is past project start or end date
        if data['start_date'] > project.end_date.replace(tzinfo=None) or data['end_date'] > project.end_date.replace(tzinfo=None):
            raise serializers.ValidationError({'error': 'Task start or end dates must not be after project end date'})
            
        return data
    
    def create(self, validated_data):
        name = validated_data.get('name')
        description = validated_data.get('description')
        label_color = validated_data.get('label_color')
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')     
           
        project = Project.objects.get(id=self.context['view'].kwargs['project_id'])
        # filter member object so that members from outside the workspace cannot be added
        member = Member.objects.filter(user=self.context['request'].user, workspace=project.workspace)
        team = Team.objects.get(id=self.context['view'].kwargs['team_id'])
                
        task = Task.objects.create(
            name=name,
            description=description,
            label_color=label_color,
            is_complete=False,
            is_team_task=True,
            start_date=start_date,
            end_date=end_date,
            project=project,
            team=team,
            created_by=member.first()
        )
        
        # add member to members list in task
        task.members.set(member)
        # task.members.set(team.members)
        task.save()
        
        return task
    

class TaskDetailSerializer(serializers.ModelSerializer):
    '''Serializer for task details'''
    
    members = MemberSerializer(read_only=True, many=True)
    
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'project', 'members', 'created_by', 'is_complete', 'is_team_task', 'team']
        
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