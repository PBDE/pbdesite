from django import forms
from django.contrib.auth.forms import BaseUserCreationForm

from django.contrib.auth.password_validation import validate_password

class LoginForm(forms.Form):

    username = forms.CharField(label="Username", max_length=64)
    password = forms.CharField(widget=forms.PasswordInput)


class CreateUser(BaseUserCreationForm):

    # need to check if the email already exists
    email = forms.EmailField()

