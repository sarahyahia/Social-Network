from django.urls import path
from .views import UserSearch, ProfileView, ProfileEditView, AddFollower, RemoveFollower, Like, Dislike, PostView, PostDetailView, PostEditView, PostDeleteView, CommentDeleteView, AddCommentLike, AddCommentDislike, CommentReplyView, PostNotification, FollowNotification, RemoveNotification



urlpatterns = [
    path('', PostView.as_view() ,name='post_list'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:post_pk>/comment/<int:pk>/like', AddCommentLike.as_view(), name='comment-like'),
    path('post/<int:post_pk>/comment/<int:pk>/dislike', AddCommentDislike.as_view(), name='comment-dislike'),
    path('post/<int:post_pk>/comment/<int:pk>/reply', CommentReplyView.as_view(), name='comment-reply'),
    path('post/<int:pk>/like', Like.as_view(), name='like'),
    path('post/<int:pk>/dislike', Dislike.as_view(), name='dislike'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>', ProfileEditView.as_view(), name='profile-edit'),
    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name='add-follower'),
    path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name='remove-follower'),
    path('search/', UserSearch.as_view(), name='profile-search'),
    path('notification/<int:notification_pk>/post/<int:post_pk>/', PostNotification.as_view(), name='post-notification'),
    path('notification/<int:notification_pk>/follow/<int:profile_pk>/', FollowNotification.as_view(), name='follow-notification'),
    path('notification/delete/<int:notification_pk>/', RemoveNotification.as_view(), name='notification-delete'),
]