from django.urls import path
from .views import PostListView, CreatePost, PostDetailView, EditPost

urlpatterns = [

    path('', PostListView.as_view(), name="feed-home"),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', CreatePost.as_view(), name="post-create"),
    path('post/<int:pk>/edit/', EditPost.as_view(), name='post-edit'),
]
