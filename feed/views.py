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
from django.db.models import F
import re

class PostListView(ListView):
	model = Post
	template_name = 'feed/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5


	def get_context_data(self, **kwargs):
		context = super(PostListView, self).get_context_data(**kwargs)
		context['all_posts'] = Post.objects.all().order_by('-date_posted')

		top_categories = Categories.objects.values().order_by('-count')[0:10]
		context['top_categories'] = [category['category'] for category in top_categories]

		filter_note_type = self.kwargs.get('type')
		filter_cat_type = self.kwargs.get('cat')

		if filter_note_type:
			context['posts'] = Post.objects.filter(note_type=filter_note_type).order_by('-date_posted')
		if filter_cat_type:
			context['posts'] = Categories.objects.get(category=filter_cat_type).post_set.values().order_by('-date_posted')

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

		insert_categories(form.instance.category, form.instance.id)

		if self.request.session.get('autocreate'):
			del self.request.session['autocreate']
			return HttpResponseRedirect(reverse('post-edit', kwargs={'pk':new_form.pk}))

		return super().form_valid(form)


@csrf_exempt
def autocreate(request):
	if request.is_ajax() and request.method == 'POST':
		data = request.POST.dict()	
		autocreate_set = data['autocreate']

		if autocreate_set == True:
			print("CREATING AUTOCREATE SESSION")
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
		insert_categories(form.instance.category, self.get_object().id)
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
		check_delete_categories(post.category,post.id)
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
			check_categories(value, post_id)
			insert_categories(value, post_id)
			Post.objects.filter(id=post_id).update(category=value)
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


def insert_categories(data, post_id):
	'''insert new categories into db or increment by one if category exists'''
	categories = format_category(data)

	for c in categories:
		try:
			cat = Categories.objects.filter(category=c)
			if not cat.exists():
				new_c = Categories()
				new_c.category = c
				new_c.count = 1
				new_c.save()
			else:
				cat.update(count=F('count')+1)
			# insert each category to the M2M db for the corresponding post object
			Post.objects.get(id=post_id).categories.add(Categories.objects.get(category=c))
		except:
			continue


def format_category(data):
	category = re.sub("[!&/\\#+()£$~%.\'\":*?<>{}]", "", data)
	category = ' '.join(category.split()).strip()

	categories = [c.lower() for c in category.split(',')]

	return categories

def check_categories(category_list,post_id):
	'''find categories listed in Post db and compare with the newly updated categories from the edited form
	if there is a category in Post that is not present from the form, reduce count of that category in the Categories db'''
	prev_cat_list = Post.objects.values().filter(id=post_id)[0]['category']

	prev_cats = [c.lower() for c in prev_cat_list.split(',')]

	current_cats = format_category(category_list)
	for c in prev_cats:
		if c not in current_cats:
			delete_category(c)

def check_delete_categories(category_list, post_id):
	'''format categories and delete accordingly'''
	categories = format_category(category_list)
	for c in categories:
		delete_category(c)


def delete_category(c):
	'''decrease category count by 1, delete if its 0'''
	new_c = Categories.objects.filter(category=c)
	if new_c.exists():
		new_c.update(count=F('count')-1)
		cat_count = new_c.values()[0]['count'] #Categories.objects.filter(category='hmmm') CHECK HERE IF ERROR
		if  cat_count <= 0:
			new_c.delete()