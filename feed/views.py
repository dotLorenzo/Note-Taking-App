from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils import timezone, dateformat
from django.views.generic import ListView, FormView, DetailView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .models import Post, Categories
from .forms import CreateForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import re

class PostListView(ListView):
	model = Post
	template_name = 'feed/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5


	def get_context_data(self, **kwargs):
		context = super(PostListView, self).get_context_data(**kwargs)
		context['all_posts'] = reversed(Post.objects.all())
		filter_note_type = self.kwargs.get('type')
		if filter_note_type:
			context['posts'] = reversed(Post.objects.filter(note_type=filter_note_type))
		return context

class PostDetailView(DetailView):
	model = Post
	context_object_name = 'post'


class CreatePost(SuccessMessageMixin, FormView):
	template_name = 'feed/form.html'
	context_object_name = 'post'
	model = Post
	form_class = CreateForm
	success_url = '/'


	def form_valid(self, form):
		form.instance.posted_by = self.request.user
		new_form = form.save()
		self.success_message =  f'New notes {form.instance.title} created.'

		if self.request.session.get('autocreate'):
			del self.request.session['autocreate']
			return HttpResponseRedirect(reverse('post-edit', kwargs={'pk':new_form.pk}))
		
		return super().form_valid(form)


@csrf_exempt
def autocreate(request):
	if request.is_ajax() and request.method == 'POST':
		data = request.POST.dict()	
		autocreate_set = data['autocreate']

		if autocreate_set:
			request.session['autocreate'] = True
		else:
			request.session.pop('autocreate', None)

	return HttpResponse("autocreate set")


class EditPostView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	model = Post
	template_name = 'feed/edit_form.html'
	context_object_name = 'post'
	fields = ['title', 'note_type', 'author', 'category', 'status', 'rating', 'notes']

	def test_func(self):
		post = self.get_object()
		# you cant update anyone elses post!
		if self.request.user == post.author:
			return True
		return False

	def form_valid(self, form):
		form.instance.date_posted = timezone.now()
		form.instance.posted_by = self.request.user
		form.save()
		self.success_message = f'Notes {form.instance.title} edited.'
		self.insert_category(form.instance.category)
		return super().form_valid(form)

class DeletePostView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
	model = Post
	success_url = '/'
	success_message = "NOTES DELETED"

	def test_func(self):
		post = self.get_object()
		# you cant update anyone elses post!
		if self.request.user == post.posted_by:
			return True
		return False


	def delete(self, request, *args, **kwargs):
		post = self.get_object()
		self.success_message = f'Notes {post.title} deleted.'
		messages.warning(self.request, self.success_message % post.__dict__)
		return super(DeletePostView, self).delete(request, *args, **kwargs)


def error_404(request, exception):
	return render(request, 'feed/404.html', {})

@csrf_exempt
def autosave_post(request):
	if request.is_ajax():
		data = request.POST.dict()
		field = data['field']
		value = data['value']
		
		try:
			post_id = int(data['id'])
			post = Post.objects.get(id=post_id)
			print(post)
		except:
			print("No matching post...")
			return HttpResponseNotFound("post does not exist")

		if "CKEDITOR" in field:
			Post.objects.filter(id=post_id).update(notes=value)
		elif "title" in field:
			Post.objects.filter(id=post_id).update(title=value)
		elif "note_type" in field:
			Post.objects.filter(id=post_id).update(note_type=value)
		elif "category" in field:
			Post.objects.filter(id=post_id).update(category=value)
			insert_categories(value)
		elif "status" in field:
			Post.objects.filter(id=post_id).update(status=value)
		elif "author" in field:
			Post.objects.filter(id=post_id).update(author=value)
		elif "rating" in field:
			Post.objects.filter(id=post_id).update(rating=value)
			
		
		date_format = dateformat.format(timezone.now(), 'H:i:s M d').split(" ", 1)
		formatted_date = f"{date_format[0]} on {date_format[1]}"
		autosave_message = f"Notes saved {formatted_date}"
		# messages.success(request, autosave_message)
		
		return HttpResponse(autosave_message)


def insert_categories(data):
	category = re.sub("[!&/\\#+()£$~%.\'\":*?<>{}]", "", data)
	category = ' '.join(category.split())

	categories = [c.title() for c in category.split(',')]

	for c in categories:
		new_c = Categories()
		new_c.category = category
		new_c.save()