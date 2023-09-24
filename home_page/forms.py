from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.password_validation import validate_password

class LoginForm(forms.Form):

    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput)


class CustomCreateUserForm(UserCreationForm):

    email = forms.EmailField()

