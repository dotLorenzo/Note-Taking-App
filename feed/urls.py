from django.urls import path
from .views import PostListView, createPost, PostDetailView

urlpatterns = [

    path('', PostListView.as_view(), name="feed-home"),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', createPost.as_view(), name="post-create"),
]
