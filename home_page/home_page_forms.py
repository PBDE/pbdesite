from django import forms
from django.contrib.auth.forms import BaseUserCreationForm

from django.contrib.auth.password_validation import validate_password

class LoginForm(forms.Form):

    username = forms.CharField(label="Username", max_length=64)
    # password = forms.PasswordInput()
    password = forms.CharField(widget=forms.PasswordInput)


# class NewUserForm(forms.Form):

#     username = forms.CharField(label="Username", max_length="64")
#     email = forms.EmailField()
#     password1 = forms.CharField(widget=forms.PasswordInput)
#     password2 = forms.CharField(widget=forms.PasswordInput)

#     def clean(self):

#         super().clean()
#         clean_pass1 = self.cleaned_data["password1"]
#         clean_pass2 = self.cleaned_data["password2"] 
#         if clean_pass1 != clean_pass2:
#             raise forms.ValidationError("Passwords must match")
#         validate_password(clean_pass1)


class CreateUser(BaseUserCreationForm):

    # need to check if the email already exists
    email = forms.EmailField()

