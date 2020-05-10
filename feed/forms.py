from django import forms
from .models import Post, Categories

class CreateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'note_type', 'author', 'category', 'status', 'rating', 'notes']
		widgets = {'category': forms.TextInput(attrs={'placeholder':'Enter comma separated categories'})}

	def clean(self):
		cleaned_data = super(CreateForm, self).clean()
		
		categories = [c.strip().title() for c in cleaned_data['category'].split(',') if c.strip()]

		for category in categories:
			self.insert_category(category)

	def insert_category(self, category):
		categories = Categories()
		categories.category = category
		categories.save()