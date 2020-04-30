from django.shortcuts import render
from django.views.generic import ListView, FormView, DetailView
from django import forms
from .models import Post
from .forms import CreateForm


class PostListView(ListView):
	model = Post
	template_name = 'feed/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

class PostDetailView(DetailView):
	model = Post
	context_object_name = 'post'
	
class CreatePost(FormView):
	template_name = 'feed/form.html'
	form_class = CreateForm
	success_url = '/'
	
	def form_valid(self, form):
		form.instance.posted_by = self.request.user
		form.save()
		return super().form_valid(form)

class EditPost(FormView):
	template_name = 'feed/edit_form.html'
	form_class = CreateForm
	success_url = '/'
	
	def form_valid(self, form):
		form.instance.posted_by = self.request.user
		form.save()
		return super().form_valid(form)


