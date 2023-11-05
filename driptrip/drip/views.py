from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import RegisterUserForm, LoginUserForm
from django.contrib.auth import authenticate, login


def home(request):
	context = {
		'sign': request.user.is_authenticated
			}

	return render(request, 'drip/home.html', context)
 
def userlogin(request):
	if request.method == "GET":
		return render(request, 'drip/login.html')
	else:
		form = LoginUserForm(request.POST) 

		if form.is_valid():
			user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
			if user is not None:
				login(request, user, backend=None)
				return redirect('home')
			else:
				return render(request, 'drip/login.html')
		else:
			return render(request, 'drip/login.html')

def register(request):
	if request.method == "GET":
		return render(request, 'drip/register.html')
	else:
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
		else:
			print(form.errors)
			return render(request, 'drip/register.html')