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
    path('productedit/', views.productedit, name='productedit'),
    path('newphoto/<int:product>', views.newphoto, name='newphoto'),
    path('newsize/<int:product>', views.newphoto, name='newsize'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>', views.remove_from_cart, name='remove_from_cart'),
    path('<str:sex_filter>/', views.home, name='home'),
]
