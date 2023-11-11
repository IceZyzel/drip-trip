from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .forms import RegisterUserForm, LoginUserForm, CreateProductForm, AddNewSize, AddNewPhoto
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

    #получаем id последнего заказа
    latest_order = Order.objects.order_by('-id').first()
    if latest_order is not None:
        order_id = latest_order.id+1
    else:
        order_id = None

    #получаем корзину
    cart = request.session.get('cart',{})  
    product_list = []

    #текущая дата
    date = datetime.now()
    
    product_photos = PhotoProduct.objects.all()
    

    for item_id in cart:
        product_id = item_id.get('id')
        product = get_object_or_404(Product, id=product_id)
        product_list.append({'product': product,})   

    
    context ={
        'cart_list': cart,
        'product_list': product_list,
        'date':date,
        'future_order_id':order_id,
        'product_photos':product_photos
    }

    
    return render(request, 'drip/cart.html',context) 

def add_to_cart(request,id):
    
        if not request.session.get('cart'):
            request.session['cart']=list()
        else:
            request.session['cart'] = list(request.session['cart'])

        
        cart_ids_list = list()
        for item in request.session['cart']:
            cart_ids_list.append(item['id'])


       # item_exist = next((item for item in request.session['cart'] if item["type"]==request.POST.get('type') and item["id"] == id), False)


        add_data = {
            #'type':request.POST.get('type'),
            'id':id
        }

        if id not in cart_ids_list :
            request.session['cart'].append(add_data)
            request.session.modified = True
        
        return render(request,'drip/cart.html')

def remove_from_cart(request,id):

    for item in request.session['cart']:
        if item['id'] == id:
            item.clear()

    while {} in request.session['cart']:
        request.session['cart'].remove({})

    if not request.session['cart']:
        del request.session['cart']

    request.session.modified = True

    return redirect('cart')

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

