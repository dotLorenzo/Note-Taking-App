from django.shortcuts import render
from django.views.generic import ListView
from .models import Post

# Create your views here.
# def home(request):

# 	return render(request, 'feed/home.html')

class PostListView(ListView):
	model = Post
	template_name = 'feed/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5