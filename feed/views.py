from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils import timezone, dateformat
from django.views.generic import ListView, FormView, DetailView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .models import Post
from .forms import CreateForm
from django.urls import reverse


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


class EditPostView(SuccessMessageMixin, UpdateView):
	model = Post
	template_name = 'feed/edit_form.html'
	context_object_name = 'post'
	fields = ['title', 'note_type', 'author', 'category', 'status', 'rating', 'notes']

	def form_valid(self, form):
		form.instance.date_posted = timezone.now()
		form.instance.posted_by = self.request.user
		form.save()
		self.success_message = f'{form.instance.title} edited.'
		return super().form_valid(form)


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