import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import RegisterUserForm, LoginUserForm, CreateProductForm, AddNewSize, AddNewPhoto
from django.contrib.auth import authenticate, login, logout
from .models import Product, PhotoProduct


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
    return render(request, 'drip/cart.html')


def exit(request):
    logout(request)

    context = {
        'sign': request.user.is_authenticated,
    }
    return render(request, 'drip/home.html', context)

def productedit(request):

    context = {
        # 'name' : "",
        # 'price' : "",
        # 'brand' : "",
        # 'description' : "",
        # 'sex' : "",
        # 'category' : "",
        # 'userclirent' : ""
    }

    if request.method == "GET":
        return render(request, 'drip/productedit.html')
    else:
        form = CreateProductForm (request.POST)

        if request.user.is_authenticated:
            if form.is_valid():
                form.instance.userclient_id = request.user.id
                p = form.save()
                new_id = p.id
                return render(request, 'drip/newsize.html', {'product' : new_id})
            else:
                print(form.errors)
                return render(request, 'drip/productedit.html', context)
        else:
            return redirect('login')
        

def newsize(request, product):
     context = {
        'product' : product
     }

     if request.method == "GET":
        return render(request, 'drip/newsize.html', context)
     else:
        form = AddNewSize (request.POST)

        if request.user.is_authenticated:
            if form.is_valid():
                form.instance.product_id = product
                form.save()

                if request.POST.get('anothersize') == 'Another size':
                    return render(request, 'drip/newsize.html', context)
                elif request.POST.get('submit-button') == 'Submit':
                    return redirect('newphoto', product)

            else:
                print(form.errors)
                return render(request, 'drip/newsize.html', context)
        else:
            return redirect('login')
        
def newphoto(request, product):    
    if request.method == "GET":
        form = AddNewPhoto()

        context = {
            'product' : product,
            'form' : form,
        }

        return render(request, 'drip/newphoto.html', context)
    else:
        context = {
            'product' : product,
        }

        print(request.POST)
        print(request.FILES)

        form = AddNewPhoto (request.POST, request.FILES)



        if request.user.is_authenticated:
            if form.is_valid():
                form.instance.product_id = product
                form.save()
                
                if request.POST.get('anotherphoto') == 'Another photo':
                    return redirect('newphoto', product)
                elif request.POST.get('submit-button') == 'Submit':
                    return render(request, 'drip/home.html', context)
            else:
                print(form.errors)
                return redirect('newphoto', product)
        else:
            return redirect('login')    