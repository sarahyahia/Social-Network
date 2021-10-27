from django.urls import path
from .views import PostView, PostDetailView, PostEditView, PostDeleteView, CommentDeleteView



urlpatterns = [
    path('', PostView.as_view() ,name='post_list'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
]