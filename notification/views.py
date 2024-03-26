from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from notification.models import Notification
from .permissions import IsNotificationOwner

from . import serializers

User = get_user_model()

class SendNotificatioView(generics.CreateAPIView):
    '''View to send a notification to another user'''
    
    serializer_class = serializers.NotificationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()
    
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class GetAllNotificationsView(generics.ListAPIView):
    '''View to get all notifications for the current logged in user'''
    
    serializer_class = serializers.NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        notifications = Notification.objects.filter(receiver=self.request.user)
        return notifications
    
    def list(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(receiver=self.request.user)
        serializer = self.serializer_class(notifications, many=True)
        
        if notifications.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You do not have any notifications at the moment'}, status=status.HTTP_204_NO_CONTENT)

class DeleteNotificationView(generics.DestroyAPIView):
    '''View to delete a notification'''
    
    serializer_class = serializers.NotificationSerializer
    permission_classes = [IsAuthenticated, IsNotificationOwner]
    
    def get_object(self):
        notification = Notification.objects.get(id=self.kwargs['notification_id'])
        self.check_object_permissions(self.request, notification)
        return notification
    
    def delete(self, request, *args, **kwargs):
        try:
            super().delete(request, *args, **kwargs)
            return Response({'message': 'Notification deleted'}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({'error': 'This notification does not exist'}, status=status.HTTP_404_NOT_FOUND)
        