from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django import forms
from .models import Post
from .forms import CreateForm

# Create your views here.
# def home(request):

# 	return render(request, 'feed/home.html')

class PostListView(ListView):
	model = Post
	template_name = 'feed/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5


class PostCreateView(CreateView):
	model = Post
	context_object_name = 'items'
	fields = ['title', 'medium', 'author', 'status', 'rating', 'category', 'notes']


def createPost(request):
	form = CreateForm()

	return render(request, 'feed/form.html', {'form':form})

