from django import forms
from .models import User, Product, Size, PhotoProduct , CATEGORY_CHOICES
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
class ProductFilterForm(forms.Form):
    brand = forms.CharField(required=False)
    category = forms.MultipleChoiceField(choices=CATEGORY_CHOICES, required=False)
    min_price = forms.FloatField(required=False)
    max_price = forms.FloatField(required=False) 

