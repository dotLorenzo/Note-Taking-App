from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from  .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.

def register(request):
	# django already provides forms for this kind of stuff ^^ UserCreationForm
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			# get submitted username if the form is valid
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}. You can now login.')
			return redirect('login') # redirect to login page after success

	else:
		form = UserRegistrationForm()
	return render (request, 'users/register.html', {'form': form})

@login_required
def profile(request):
	if request.method == 'POST':
		# setting instance = ... will populate the fields
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, 
									request.FILES, 
									instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, 'Account updated!.')
			# stop post-get redirect pattern. Reloading the page makes browser send a GET req
			# so if we reload we wont send a POST and get a browser warning for re-sending data
			return redirect('profile')

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	context = {
		'u_form': u_form,
		'p_form': p_form
	}

	return render(request, 'users/profile.html', context)