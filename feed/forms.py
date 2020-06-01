from django import forms
from .models import Post, Categories
import re

class CreateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'note_type', 'author', 'category', 'status', 'rating', 'notes']
		widgets = {'category': forms.TextInput(attrs={'placeholder':'Enter comma separated categories'})}
		
	# def clean(self):
	# 	cleaned_data = super(CreateForm, self).clean()
		
	# 	category = cleaned_data['category'].replace("[!&/\\#+()£$~%.\'\":*?<>{}]", " ")
	# 	category = ' '.join(category.split())

	# 	categories = [c.title() for c in category.split(',')]

	# 	for category in categories:
	# 		self.insert_category(category)
 
	def clean_title(self):
		data  = self.cleaned_data['title']
		title = ' '.join(data.split())

		return title

	def clean_category(self):
		data = self.cleaned_data['category']
		category = re.sub("[!&/\\#+()£$~%.\'\":*?<>{}]", "", data)
		category = ' '.join(category.split())

		categories = [c.title() for c in category.split(',')]

		for c in categories:
			self.insert_category(c)

		return category

	def insert_category(self, category):
		categories = Categories()
		categories.category = category
		categories.save()