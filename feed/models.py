from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse

# Create your models here.

# Post content to server model


class Categories(models.Model):
	category = models.CharField(max_length=100)

	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.category


class Post(models.Model):
	type_choices = [
		('book', 'Book'),
		('doc', 'Documentary'),
		('thinker', 'Thinker/Person'),
		('misc','Other/Miscellaneous'),
		(None, 'Select type...')
	]
	rating_choices = [
		(1, 1),
		(2, 2),
		(3, 3),
		(4, 4),
		(5, 5)
	]
	status_choices = [
		('to do', 'to do'),
		('in progress', 'in progress'),
		('completed', 'completed')
	]
	title = models.CharField(max_length=100)
	note_type = models.CharField(max_length=100,choices=type_choices,null=True)
	# categories = models.ManyToManyField(Categories)
	category = models.CharField(max_length=100, null=True)
	author = models.CharField(max_length=100, default='', blank=True)
	notes = RichTextField()
	status = models.CharField(
		max_length=100,
		choices=status_choices,
		default='to do'
		)
	rating = models.IntegerField(
		choices=rating_choices,
		default=5
	)
	date_posted = models.DateTimeField(default=timezone.now)
	posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk':self.pk})


