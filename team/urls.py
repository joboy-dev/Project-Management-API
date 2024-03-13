from django.urls import path
from .import views

app_name = 'team'

urlpatterns = [
    path('create/project/<uuid:project_id>/', views.CreateTeamView.as_view(), name='create-team'),
    path('<uuid:team_id>/', views.TeamDetailsView.as_view(), name='team-details'),
    path('project/<uuid:project_id>/all/', views.GetAllProjectTeams.as_view(), name='all-teams-in-project'),
    path('<uuid:team_id>/member/<uuid:member_id>/add/', views.AddMemberToTeamView.as_view(), name='add-team-member'),
    path('<uuid:team_id>/member/<uuid:member_id>/remove/', views.RemoveMemberFromTeamView.as_view(), name='remove-team-member'),
]