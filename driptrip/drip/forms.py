from dataclasses import field
from datetime import datetime
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField


class RegisterUserForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = 'username', 'email', 'password1', 'password2'

class LoginUserForm(forms.Form):
    username = UsernameField()
    password = forms.CharField()

class CreateOrderForm(forms.ModelForm):   
    full_name = forms.CharField(max_length=64)
    adress = forms.CharField(max_length=64)
    phone_number = forms.CharField(max_length=64)   

    class Meta:
        model = Order
        fields = ['full_name', 'phone_number', 'adress','date']
        

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'brand', 'description', 'sex', 'category']
        exclude = ['User']

class AddNewSize(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['size', 'count']
        exclude = ['product']

class AddNewPhoto(forms.ModelForm):
    class Meta:
        model = PhotoProduct
        fields = ['photolink']
        exclude = ['product']



