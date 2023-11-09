from datetime import datetime
from django.db.models import Max
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import RegisterUserForm, LoginUserForm
from django.contrib.auth import authenticate, login, logout
from .models import *


def home(request, sex_filter = None):
    if(sex_filter == None):
        products = Product.objects.all()  # Извлекаем все продукты
    else:
        products = Product.objects.filter(sex=sex_filter)  # Извлекаем продукты по фильтру
    
    context = {
        'sign': request.user.is_authenticated,
        'products': products,  # Добавляем переменную products в контекст
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
            return redirect('Userlogin')
        else:
            print(form.errors)
            return render(request, 'drip/register.html')


def cart(request):
    
    # order_id = Order.objects.all().order_by('-id').id


    date = datetime.date
    context = {        
        'future_order_id': 1,
        'date':date,
    }
    return render(request, 'drip/cart.html', context)


def exit(request):
    logout(request)

    context = {
        'sign': request.user.is_authenticated,
    }
    return render(request, 'drip/home.html', context)
