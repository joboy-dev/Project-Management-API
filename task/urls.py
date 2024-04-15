from django.urls import path
from .import views

app_name = 'task'

urlpatterns = [
    path('create/project/<uuid:project_id>/', views.CreateProjectTaskView.as_view(), name='create-general-task'),
    path('create/project/<uuid:project_id>/team/<uuid:team_id>/', views.CreateTeamTaskView.as_view(), name='create-team-task'),
    path('team/<uuid:team_id>/', views.GetTasksForTeamView.as_view(), name='tasks-for-team'),
    path('project/<uuid:project_id>/', views.GetProjectTasksView.as_view(), name='tasks-for-project'),
    path('<uuid:task_id>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('<uuid:task_id>/member/<uuid:member_id>/add/', views.AddMemberToTaskView.as_view(), name='add-task-member'),
    path('<uuid:task_id>/member/<uuid:member_id>/remove/', views.RemoveMemberFromTaskView.as_view(), name='remove-task-member'),
    path('<uuid:task_id>/toggle-completion-status/', views.ToggleCompletionStatusView.as_view(), name='toggle-completion-status'),
]