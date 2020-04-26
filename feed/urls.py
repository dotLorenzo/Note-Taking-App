from django.urls import path
from .views import PostListView, createPost

urlpatterns = [

    path('', PostListView.as_view(), name="feed-home"),
    path('post/new/', createPost, name="post-create"),
]
