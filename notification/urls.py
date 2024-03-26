from django.urls import path
from . import views

app_name = 'notification'
urlpatterns = [
    path('send/<uuid:user_id>/', views.SendNotificatioView.as_view(), name='send-notification'),
    path('all/', views.GetAllNotificationsView.as_view(), name='get-notifications'),
    path('<uuid:notification_id>/delete/', views.DeleteNotificationView.as_view(), name='delete-notification'),
]