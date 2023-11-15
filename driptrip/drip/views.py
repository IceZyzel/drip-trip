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


def product(request, id, selected_image_id = None):

    product = Product.objects.get(id = id)
    product_photos = PhotoProduct.objects.filter(product_id = id)
    sizes = Size.objects.filter(product_id = id)
    seller = User.objects.get(id=product.userclient_id)

    if (selected_image_id==None):
        main_photo = product_photos.first()
    else:
        main_photo = product_photos.get(id = selected_image_id)

    context = {
        'product': product,
        'product_photos': product_photos,
        'main_photo': main_photo,
        'sizes': sizes,
        'seller':seller,
    }


    return render(request,'drip/product.html', context)


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
    
    #получаем фото товаров
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
    if request.method == 'POST':
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
        
    return redirect(request.POST.get('url_from'))

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

def newproduct(request):
    if request.method == "GET":
        return render(request, 'drip/newproduct.html')
    else:
        form = CreateProductForm (request.POST)

        if request.user.is_authenticated:
            if form.is_valid():
                form.instance.user_id = request.user.id
                p = form.save()
                new_id = p.id
                return render(request, 'drip/newsize.html', {'product' : new_id})
            else:
                print(form.errors)
                return render(request, 'drip/newproduct.html')
        else:
            return redirect('Userlogin')
        
def all_my_products(request):
    products = Product.objects.filter(user = request.user.id)

    context = {
        'sign': request.user.is_authenticated,
        'products': products,  
    }

    if request.method == "GET":
        return render(request, 'drip/all_my_products.html', context)
        
def editproduct(request, product): 
    sizes_forms = []

    if request.method == "GET":        
        product_to_edit = Product.objects.get(id = product)

        sizes = Size.objects.filter(product = product_to_edit)
        sizes_forms = []
        for s in sizes:
            sizes_forms.append((AddNewSize(instance=s), s.pk))

        photos = PhotoProduct.objects.filter(product = product_to_edit)
        photos_forms = []
        for ph in photos:
            photos_forms.append((AddNewPhoto(instance=ph), ph.pk))

        context = {
            'product_to_edit': product_to_edit,
            'sizes_forms': sizes_forms,
            'photos_forms' : photos_forms
        }

        return render(request, 'drip/editproduct.html', context)
    else:     
        item = Product.objects.get(id = product)
        form = CreateProductForm(request.POST, instance=item)

        

        if form.is_valid():
            form.save()

        return redirect('all_my_products')
    
def deleteproduct(request, product):
    product_to_delete = Product.objects.get(id = product)
    product_to_delete.delete()
    return redirect('all_my_products')

def addsize(request, product):
     context = {
        'product' : product,
        'flag' : True
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
                    return redirect('editproduct', product)

            else:
                print(form.errors)
                return render(request, 'drip/newsize.html', context)
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
        
def deletesize(request, size):
    size_to_delete = Size.objects.get(pk = size)
    product = size_to_delete.product.pk
    size_to_delete.delete()
    return redirect('editproduct', product)

def addphoto(request, product):    
    if request.method == "GET":
        form = AddNewPhoto()

        context = {
            'product' : product,
            'form' : form,
            'flag' : True,
        }

        return render(request, 'drip/newphoto.html', context)
    else:
        context = {
            'product' : product,
            'flag' : True,
        }

        form = AddNewPhoto (request.POST, request.FILES)

        if request.user.is_authenticated:
            if form.is_valid():
                form.instance.product_id = product
                form.save()
                
                if request.POST.get('anotherphoto') == 'Another photo':
                    return redirect('newphoto', product)
                elif request.POST.get('submit-button') == 'Submit':
                    return redirect('editproduct', product)
            else:
                print(form.errors)
                return redirect('newphoto', product)
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

        form = AddNewPhoto (request.POST, request.FILES)

        if request.user.is_authenticated:
            if form.is_valid():
                form.instance.product_id = product
                form.save()
                
                if request.POST.get('anotherphoto') == 'Another photo':
                    return redirect('newphoto', product)
                elif request.POST.get('submit-button') == 'Submit':
                    return redirect('home')
            else:
                print(form.errors)
                return redirect('newphoto', product)
        else:
            return redirect('login')    
        
def deletephoto(request, photo):
    photo_to_delete = PhotoProduct.objects.get(pk = photo)
    product = photo_to_delete.product.pk
    photo_to_delete.delete()
    return redirect('editproduct', product)

