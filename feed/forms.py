from django import forms
from .models import Post, Categories
import re
from django.db.models import F

class CreateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'note_type', 'author', 'category', 'status', 'rating', 'notes']
		widgets = {'category': forms.TextInput(attrs={'placeholder':'Enter comma separated categories'})}

	def __init__(self, *args, **kwargs):
		super(CreateForm, self).__init__(*args, **kwargs)
 
	def clean_title(self):
		data  = self.cleaned_data['title']
		title = ' '.join(data.split())

		return title

	# def clean_category(self):
	# 	print(self.post_id)
	# 	data = self.cleaned_data['category']
	# 	category = re.sub("[!&/\\#+()£$~%.\'\":*?<>{}]", "", data)
	# 	category = ' '.join(category.split()).strip()

	# 	categories = [c.lower() for c in category.split(',')]

	# 	self.insert_categories(categories, post_id)

	# 	return category


	# def insert_categories(self, categories, post_id):
	# 	'''insert new categories into Post db and M2M db or increment by one if category exists'''
	# 	for c in categories:
	# 		try:
	# 			cat = Categories.objects.filter(category=c)
	# 			if not cat.exists():
	# 				new_c = Categories()
	# 				new_c.category = c
	# 				new_c.count = 1
	# 				new_c.save()
	# 			else:
	# 				cat.update(count=F('count')+1)
	# 			# insert each category to the M2M db for the corresponding post object
	# 			Post.objects.get(id=post_id).categories.add(Categories.objects.get(category=c))
	# 		except:
	# 			continue