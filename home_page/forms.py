from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):

    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput)


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username"
        )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username"
        )

