from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('account/register/', views.RegisterView.as_view(), name='register'),
    path('account/login/', views.LoginView.as_view(), name='login'),
    path('account/email/verify/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('account/email/verify/resend/', views.ResendVerificationEmailView.as_view(), name='resent-verification'),
    path('account/details/', views.UserDetailsView.as_view(), name='user-details'),
    path('account/email/change/', views.ChangeEmailView.as_view(), name='change-email'),
    path('account/password/change/', views.ChangePasswordView.as_view(), name='change-password'),
    path('account/logout/', views.LogoutView.as_view(), name='logout'),
]