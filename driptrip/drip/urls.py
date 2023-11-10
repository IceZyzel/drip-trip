from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.userlogin, name='Userlogin'),
    path('register/', views.register, name='register'),
    path('cart/', views.cart, name='Cart'),
    path('exit/', views.exit, name='exit'),
    path('productedit/', views.productedit, name='productedit'),
    path('newsize/<int:product>', views.newsize, name='newsize'),
    path('<str:sex_filter>/', views.home, name='home'),
]
