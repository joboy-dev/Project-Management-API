from django.urls import path
from .import views

app_name = 'task'

urlpatterns = [
    path('create/project/<uuid:project_id>/', views.CreateGeneralProjectTaskView.as_view(), name='create-general-task'),
    path('create/project/<uuid:project_id>/team/<uuid:team_id>/', views.CreateTeamTaskView.as_view(), name='create-team-task'),
    path('team/<uuid:team_id>/', views.GetTasksForTeamView.as_view(), name='tasks-for-team'),
    # path('<uuid:team_id>/member/<uuid:member_id>/add/', views.AddMemberToTeamView.as_view(), name='add-team-member'),
    # path('<uuid:team_id>/member/<uuid:member_id>/remove/', views.RemoveMemberFromTeamView.as_view(), name='remove-team-member'),
]