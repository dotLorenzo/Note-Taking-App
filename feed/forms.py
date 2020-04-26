from django import forms
from .models import Post

class CreateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'medium', 'author', 'categories', 'status', 'rating', 'notes']
		widgets = {'author': forms.HiddenInput(),
					'rating': forms.HiddenInput()}
