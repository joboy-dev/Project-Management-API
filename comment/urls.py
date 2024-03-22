from django.urls import path

from . import views

app_name = 'comment'
urlpatterns = [
    path('create/<uuid:project_id>/', views.CreateCommentView.as_view(), name='create-comment'),
    path('<uuid:comment_id>/reply/', views.CreateCommentReplyView.as_view(), name='create-comment-reply'),
    path('<uuid:comment_id>/', views.CommentDetailsView.as_view(), name='comment-details'),
    path('<uuid:comment_reply_id>/', views.CommentReplyDetailsView.as_view(), name='comment-reply-details'),
    path('all/', views.GetAllCommentsView.as_view(), name='all-comments'),
    path('<uuid:comment_id>/replies/', views.GetAllCommentRepliesView.as_view(), name='all-comments'),
]