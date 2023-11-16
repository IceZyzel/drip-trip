from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.userlogin, name='Userlogin'),
    path('register/', views.register, name='register'),
    path('cart/', views.cart, name='cart'),
    path('create_order/', views.create_order, name='create_order'),
    path('exit/', views.exit, name='exit'),
    path('product/<int:id>', views.product, name='product'),
    path('newproduct/', views.newproduct, name='newproduct'),
    path('all_my_products/', views.all_my_products, name='all_my_products'),
    path('editproduct/<int:product>', views.editproduct, name='editproduct'),
    path('deleteproduct/<int:product>', views.deleteproduct, name='deleteproduct'),
    path('newphoto/<int:product>', views.newphoto, name='newphoto'),
    path('addphoto/<int:product>', views.addphoto, name='addphoto'),
    path('deletephoto/<int:photo>', views.deletephoto, name='deletephoto'),
    path('newsize/<int:product>', views.newsize, name='newsize'),
    path('addsize/<int:product>', views.addsize, name='addsize'),
    path('deletesize/<int:size>', views.deletesize, name='deletesize'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>', views.remove_from_cart, name='remove_from_cart'),
    path('<str:sex_filter>/', views.home, name='home'),
]
