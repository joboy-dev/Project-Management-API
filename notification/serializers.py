from django.contrib.auth import get_user_model
from rest_framework import serializers

from notification.models import Notification
from user.serializers import UserDetailsSerializer

User = get_user_model()

class NotificationSerializer(serializers.ModelSerializer):
    '''Serializer for notifications'''
    
    sender = UserDetailsSerializer(read_only=True)
    receiver = UserDetailsSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['id', 'sender', 'receiver']
        
    def create(self, validated_data):
        notification = Notification.objects.create(
            message = validated_data.get('message'),
            sender = self.context['request'].user,
            receiver = User.objects.get(id=self.context['view'].kwargs['user_id'])
        )
        
        return notification