from django.urls import path
from . import views

app_name = 'workspace'

urlpatterns = [
    path('create/', views.CreateWorkspaceView.as_view(), name='create-workspace'),
    path('<uuid:workspace_id>/', views.WorkspaceDetailsView.as_view(), name='workspace-details'),
    path('<uuid:workspace_id>/subscription/update/', views.UpdateWorkspaceSubscriptionView.as_view(), name='update-workspace-subscription'),
    path('<uuid:workspace_id>/member/<uuid:user_id>/add/', views.AddMemberToWorkspaceView.as_view(), name='add-member'),
    path('<uuid:workspace_id>/member/<uuid:member_id>/remove/', views.RemoveMemberFromWorkspaceView.as_view(), name='remove-member'),
    path('<uuid:workspace_id>/members/', views.GetWorkspaceMembersView.as_view(), name='get-workspace-members'),
    path('<uuid:workspace_id>/member/<uuid:member_id>/update/', views.UpdateMemberRoleView.as_view(), name='get-workspace-members'),
]