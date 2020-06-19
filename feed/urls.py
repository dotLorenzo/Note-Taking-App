from django.urls import path
from django.conf.urls import handler404
from django.conf.urls.static import static
from .views import (
	PostListView, 
	CreatePost, 
	PostDetailView, 
	EditPostView,
	DeletePostView, 
	error_404,
	autosave_post,
	autocreate
	)

urlpatterns = [

    path('', PostListView.as_view(), name="feed-home"),
    path('type/<str:type>/', PostListView.as_view(), name="feed-home-filter-type"),
    path('category/<str:cat>/', PostListView.as_view(), name="feed-home-filter-category"),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', CreatePost.as_view(), name="post-create"),
    path('post/<int:pk>/edit/', EditPostView.as_view(), name='post-edit'),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name='post-delete'),
    path('post/autosave/', autosave_post, name='post-autosave'),
    path('post/autocreate/', autocreate, name='post-autocreate')
]