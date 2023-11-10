from django import forms
from .models import User, Product, Size, PhotoProduct
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

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'brand', 'description', 'sex', 'category']
        exclude = ['UserClient']

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
