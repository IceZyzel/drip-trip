from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import RegisterUserForm


def home(request):
	return HttpResponse('<h1>Home</h1>')
 
def login(request):
	if request.method == "GET":
		return render(request, 'drip/login.html')
	else:
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			#username = form.cleaned_data.get('username')
			#messages.success(request, f'Создан аккаунт {username}!')
			return redirect('login')
		else:
			print(form.errors)
			return render(request, 'drip/login.html')

def register(request):
	if request.method == "GET":
		return render(request, 'drip/register.html')
	else:
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			#username = form.cleaned_data.get('username')
			#messages.success(request, f'Создан аккаунт {username}!')
			return redirect('login')
		else:
			print(form.errors)
			return render(request, 'drip/register.html')