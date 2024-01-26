from django.contrib.auth import get_user_model
from rest_framework import serializers
from workspace.models import Member, Workspace

User = get_user_model()

class CreateWorkspaceSerializer(serializers.ModelSerializer):
    '''Serializer to create a new workspace'''
    
    creator = serializers.SerializerMethodField(read_only=True)
    
    def get_creator(self, obj):
        return obj.creator.email
    
    class Meta:
        model = Workspace
        fields = ['id', 'name', 'company_email', 'no_of_members_allowed', 'creator']
        read_only_fields = ['id', 'creator']
        
    def validate(self, data):
        if Workspace.objects.filter(company_email=data['company_email']).exists():
            raise serializers.ValidationError({'error': 'This email is in use by another workspace'})
        
        # check if workspace creator is already in another workspace
        if Member.objects.filter(user=self.context['request'].user).exists():
            raise serializers.ValidationError({'error': 'You are entitled to one workspace at a time.'})
        
        return data
        
    def create(self, validated_data):
        name = validated_data.get('name')
        company_email = validated_data.get('company_email')
        no_of_members_allowed = validated_data.get('no_of_members_allowed')
        creator = self.context['request'].user
        
        # create workspace
        workspace = Workspace.objects.create(
            name=name,
            company_email=company_email,
            no_of_members_allowed=no_of_members_allowed,
            creator=creator,
        )
        
        # Add creator to member list
        Member.objects.create(
            user=creator,
            workspace=workspace,
            role='editor',
        )
        
        # Increase number of members by 1
        workspace.current_no_of_members += 1
        workspace.save()
        
        return workspace
    

class WorkspaceDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for handling workspace details'''
    
    creator = serializers.SerializerMethodField(read_only=True)
    
    def get_creator(self, obj):
        return obj.creator.email
    
    class Meta:
        model = Workspace
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'current_no_of_members']
        
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
            
        instance.save()
        return instance
    

class MemberSerializer(serializers.ModelSerializer):
    '''Serializer to add a member to a workspace and also get all members in a workspace'''
    
    workspace = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    
    def get_workspace(self, obj):
        return obj.workspace.name
    
    def get_user(self, obj):
        return obj.user.email
    
    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ['user', 'workspace', 'date_joined']
        
    def create(self, validated_data):
        workspace_id = self.context['view'].kwargs['workspace_id']
        user_id = self.context['view'].kwargs['user_id']
        
        workspace = Workspace.objects.get(id=workspace_id)
        user = User.objects.get(id=user_id)
        role = validated_data.get('role')
        
        # check if user you want to add is already in another workspace
        if Member.objects.filter(user=user).exists():
            raise serializers.ValidationError({'error': 'The user is already in a workspace'})
        
        # check if workspace is full
        if workspace.current_no_of_members < workspace.no_of_members_allowed:
            member = Member.objects.create(
                workspace=workspace,
                user=user,
                role=role,
            )
            
            workspace.current_no_of_members += 1
            workspace.save()
            
            return member
        else:
            raise serializers.ValidationError({'error': 'The workspaace is full'})
    
    
class UpdateMemberSerializer(serializers.ModelSerializer):
    '''Serializer to update member role'''
    
    workspace = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    
    def get_workspace(self, obj):
        return obj.workspace.name
    
    def get_user(self, obj):
        return obj.user.email
    
    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ['user', 'workspace', 'date_joined']
        
    def validate(self, data):
        user_id = self.context['view'].kwargs['user_id']
        user = User.objects.get(id=user_id)
        
        if user == self.context['request'].user:
            raise serializers.ValidationError({'error': 'You cannot edit your own role'})
        return data
        
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        instance.save()
        return instance