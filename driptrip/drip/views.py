from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

def home(request):
	return HttpResponse('<h1>Home</h1>')
 
def login(request):
	return render(request, 'drip/login.html')

def register(request):
	return render(request, 'drip/register.html')

