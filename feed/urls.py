from django.urls import path
from django.conf.urls import handler404
from django.conf.urls.static import static
from .views import (
	PostListView, 
	CreatePost, 
	PostDetailView, 
	EditPostView, 
	error_404,
	autosave_post
	)

urlpatterns = [

    path('', PostListView.as_view(), name="feed-home"),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', CreatePost.as_view(), name="post-create"),
    path('post/<int:pk>/edit/', EditPostView.as_view(), name='post-edit'),
    path('post/autosave/', autosave_post, name='post-autosave')
]