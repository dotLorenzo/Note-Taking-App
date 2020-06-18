from django import forms
from .models import Post, Categories
import re
from django.db.models import F

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
		category = ' '.join(category.split()).strip()

		categories = [c.lower() for c in category.split(',')]

		self.insert_categories(categories)

		return category


	def insert_categories(data):
		'''insert new categories into db or increment by one if category exists'''
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
			except:
				continue