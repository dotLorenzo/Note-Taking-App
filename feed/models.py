from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

# Post content to server model


class Category(models.Model):
	category = models.CharField(max_length=100)

	def __str__(self):
		return self.category


class Post(models.Model):
	type_choices = [
		('book', 'book'),
		('doc', 'documentary'),
		('thinker', 'thinker/person')
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
	_type = models.CharField(max_length=100,choices=type_choices)
	category = models.ManyToManyField(Category)
	author = models.CharField(max_length=100)
	notes = models.TextField()
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
