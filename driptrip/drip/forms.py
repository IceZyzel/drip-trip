from django import forms
from django.core.exceptions import ValidationError

from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

class LoginUserForm(forms.Form):
    username = UsernameField()
    password = forms.CharField()

class CreateOrderForm(forms.ModelForm):   
    full_name = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Full name'}))
    adress = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    phone_number = forms.CharField(max_length=12, widget=forms.TextInput(attrs={'placeholder': '0505005555'}))
    
    class Meta:
        model = Order
        fields = ['adress', 'full_name', 'phone_number']
        exclude = ['User', 'usercourier','date', 'status']
    
    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if any(char.isdigit() for char in full_name):
            raise ValidationError('Повне ім`я не повинно мати цифри')
        parts = full_name.split()
        if len(parts) != 2:
            raise ValidationError('Введіть Імя та Прізвище через пробіл')
        return full_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if len(phone_number) != 10 or not phone_number.startswith('0') or not phone_number.isdigit():
            raise ValidationError('Номер телефону має невірний формат')
        return phone_number

    def clean_address(self):
        address = self.cleaned_data['address']

        if len(address) < 8:
            raise ValidationError('Адреса повинна мати не меньше, ніж 8 символів')
        if address.isdigit():
            raise ValidationError('Введіть справжню адресу')
        return address


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

