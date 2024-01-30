from django.urls import path
from .import views

app_name = 'team'

urlpatterns = [
    path('create/project/<uuid:project_id>/', views.CreateTeamView.as_view(), name='create-team'),
    path('<uuid:team_id>/', views.TeamDetailsView.as_view(), name='team-details'),
]