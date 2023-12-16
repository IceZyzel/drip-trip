from asyncio.windows_events import NULL
from datetime import datetime
from pickle import NONE
from types import NoneType

from django.db.models import F
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import *


def home(request, sex_filter=None):
    if sex_filter is None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(sex=sex_filter)

    product_list = []

    for product in products:
        product_photo = PhotoProduct.objects.filter(product_id=product.id).first()
        product_list.append({'product_photo': product_photo})

    # Handle form submission
    if request.method == 'GET':
        form = ProductFilterForm(request.GET)
        if form.is_valid():
            # Filter products based on form data
            brand = form.cleaned_data.get('brand')
            category = form.cleaned_data.get('category')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')

            if brand:
                products = products.filter(brand__icontains=brand)

            if category:
                products = products.filter(category__in=category)

            if min_price:
                products = products.filter(price__gte=min_price)

            if max_price:
                products = products.filter(price__lte=max_price)

            # Handle search query
            search_query = request.GET.get('search', '')
            if search_query:
                products = products.filter(name__icontains=search_query)

    else:
        form = ProductFilterForm()

    context = {
        'sign': request.user.is_authenticated,
        'products': products,
        'product_list': product_list,
        'filter_form': form,
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
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Userlogin')
    else:
        form = RegisterUserForm()

    return render(request, 'drip/register.html', {'form': form})

def product(request, id, size_id=None ,selected_image_id = None):

    product = Product.objects.get(id = id)
    product_photos = PhotoProduct.objects.filter(product_id = id)
    sizes = Size.objects.filter(product_id = id, count__gt=0)
    seller = User.objects.get(id=product.user_id)
    selected_size_id = size_id


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
        'selected_size_id':selected_size_id,
    }


    return render(request,'drip/product.html', context)


def cart(request):
 
    #получаем id последнего заказа
    latest_order = Order.objects.order_by('-id').first()
    if latest_order is not None:
        order_id = latest_order.id+1
    else:
        order_id = 1
    #получаем корзину
    cart = request.session.get('cart',{})  

    product_list = []
    order_products = []
    #текущая дата
    date = datetime.now()
    form = CreateOrderForm()
    error =""
    #получаем фото товаров
    product_photos = PhotoProduct.objects.all()
    
    print(cart)
    for item_id in cart:
        product_id = item_id.get('id')
        size_id = item_id.get('size_id')
        size = Size.objects.get(id = size_id)
        product = get_object_or_404(Product, id=product_id)
        seller = User.objects.get(id=product.user_id)
        product_photo = PhotoProduct.objects.filter(product_id = product_id).first()
        orderproduct = OrderProduct(order_id = order_id, product_id = product_id, size_name = size.size)

        order_products.append(orderproduct)
        product_list.append({'product': product,'seller':seller, 'product_photo': product_photo ,'size':size})   
    


    if request.method == 'POST':
        if request.user.is_authenticated:
            if not cart:
                error='Cart is empty'
            else:
                form = CreateOrderForm(request.POST)
                form.instance.user_id = request.user.id
                form.instance.status = 'New'

                if(form.is_valid()):
                    form.save()

                    for order_product in order_products:
                        order_product.save()

                    for element in product_list:
                        size_to_delete = element.get('size')
                        size_to_delete.count = F('count') - 1
                        size_to_delete.save()
                        print(size_to_delete)

                    del request.session['cart']
                    return redirect('home')
                else:
                    print(form.errors)
                    error='Incorrect value of fields'
        else:
            return redirect('Userlogin')
    
        
    context ={
        'cart_list': cart,
        'product_list': product_list,
        'date':date,
        'future_order_id':order_id,
        'product_photos':product_photos,
        'form':form,
        'error':error,
    }
    
    
    return render(request, 'drip/cart.html',context) 



def add_to_cart(request, id, size_id='None' ):
    if request.method == 'POST':
        if not request.session.get('cart'):
            request.session['cart']=list()
        else:
            request.session['cart'] = list(request.session['cart'])

        cart_ids_list = list()
        for item in request.session['cart']:
            cart_ids_list.append(item['id'])
            cart_ids_list.append(item['size_id'])
        
        #item_exist = next((item for item in request.session['cart'] if item["type"]==request.POST.get('type') and item["id"] == id), False)

        add_data = {
            'size_id':size_id,
            'id':id,
        }   
        print(add_data['size_id'])

        if (add_data['size_id'] != 'None'):

            if size_id not in cart_ids_list:
                request.session['cart'].append(add_data)
                request.session.modified = True
        


    return redirect(request.POST.get('url_from'))

def remove_from_cart(request,id,size_id):

    for item in request.session['cart']:
        if item['id'] == id and item['size_id'] == str(size_id):
            item.clear()

    while {} in request.session['cart']:
        request.session['cart'].remove({})

    if not request.session['cart']:
        del request.session['cart']

    request.session.modified = True

    return redirect('cart')



def delete_cart(request):
    if request.session.get('cart'): 
        del request.session['cart']  
    return redirect('cart') 



def exit(request):
    logout(request)

    context = {
        'sign': request.user.is_authenticated,
    }
    return render(request, 'drip/home.html', context)

def newproduct(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, 'drip/newproduct.html')
        else:
            return redirect('Userlogin')
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
        if request.user.is_authenticated:
            return render(request, 'drip/all_my_products.html', context)
        else:
            return redirect('Userlogin')
        
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

        count = 0

        size_list = request.POST.getlist('size')
        count_list = request.POST.getlist('count')
        print(size_list)
        print(count_list)

        for size in Size.objects.filter(product=item):
            size_form = AddNewSize({'size': size_list[count], 'count': count_list[count]}, instance=size)
            if size_form.is_valid():
                size_form.save()
                count += 1

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
                    return redirect('addphoto', product)
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

