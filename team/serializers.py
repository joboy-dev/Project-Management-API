from rest_framework import serializers
from project.models import Project

from team.models import Team
from workspace.models import Member

class CreateTeamSerializer(serializers.ModelSerializer):
    '''Serializer for handling creation of team'''
    
    class Meta:
        model = Team
        fields = '__all__'
        read_only_fields = ['id', 'project', 'members', 'created_by']
        
    def create(self, validated_data):
        name = validated_data.get('name')
        team_pic = validated_data.get('team_pic')
        project = Project.objects.get(id=self.context['view'].kwargs['project_id'])
        member = Member.objects.filter(user=self.context['request'].user)

        # check if member is in project members list
        if not project.members.contains(member.first()):
            raise serializers.ValidationError({'error': 'You are not a part of this project so you cannot create a team'})
        
        if member.first().role != 'editor':
            raise serializers.ValidationError({'error': 'You are not an editor in the workspace'})
        
        team = Team.objects.create(
            name=name,
            team_pic=team_pic,
            project=project,
            created_by=member.first(),
        )
        
        team.members.set(member)
        team.save()
        
        return team
    

class TeamDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for team details'''
    
    class Meta:
        model = Team
        fields = '__all__'
        read_only_fields = ['id', 'project', 'members', 'created_by']
        
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
            
        instance.save()
        return instance