from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from django.views.generic import ListView, FormView, DetailView, UpdateView
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
	
class CreatePost(SuccessMessageMixin, FormView):
	template_name = 'feed/form.html'
	form_class = CreateForm
	success_url = '/'
	
	def form_valid(self, form):
		form.instance.posted_by = self.request.user
		form.save()
		self.success_message =  f'New notes {form.instance.title} created.'
		return super().form_valid(form)


class EditPostView(SuccessMessageMixin, UpdateView):
	model = Post
	template_name = 'feed/edit_form.html'
	fields = ['title', 'note_type', 'author', 'category', 'status', 'rating', 'notes']

	def form_valid(self, form):
		form.instance.date_posted = timezone.now()
		form.instance.posted_by = self.request.user
		form.save()
		self.success_message = f'{form.instance.title} edited.'
		return super().form_valid(form)


def error_404(request, exception):
	return render(request, 'feed/404.html', {})


