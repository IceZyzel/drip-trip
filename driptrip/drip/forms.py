from django import forms
from .models import User
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