from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, CustomUserCreationForm

INDEX_TEMPLATE = "home_page/index.html"
REGISTER_TEMPLATE = "home_page/register.html"
LOGIN_TEMPLATE = "home_page/login.html"
ACCOUNT_TEMPLATE = "home_page/account.html"
DELETE_ACCOUNT_TEMPLATE = "home_page/delete_account.html"

def index(request):
    return render(request, INDEX_TEMPLATE)

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home_page:account', 
                                            kwargs={"user": request.user.username})
        )
    if request.method == "POST":
        new_user_form = CustomUserCreationForm(request.POST)
        if new_user_form.is_valid():
            user = get_user_model().objects.create_user(new_user_form.cleaned_data["username"], 
                                                        new_user_form.cleaned_data["email"], 
                                                        new_user_form.cleaned_data["password1"])
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse(
                    "home_page:account", 
                    args=[new_user_form.cleaned_data["username"]]
                    )
                )
        return render(request, REGISTER_TEMPLATE, {
            "form": new_user_form
        })
    return render(request, REGISTER_TEMPLATE, {
        "form": CustomUserCreationForm()
    })

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home_page:account', 
                                            kwargs={"user": request.user.username})
        )
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("home_page:account", 
                                                    kwargs={"user": username})
                )
        return render(request, 
                      LOGIN_TEMPLATE, 
                      {"form": login_form, "message": "Details did not match an existing user"}
        )
    return render(request, LOGIN_TEMPLATE, {
        "form": LoginForm()
    })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home_page:index"))

def user_view(request, user):
    if request.user.is_authenticated and user == request.user.username:
        return render(request, ACCOUNT_TEMPLATE)
    elif get_user_model().objects.filter(username=user).exists():
        return HttpResponseRedirect(reverse("home_page:login"))
    return HttpResponseRedirect(reverse("home_page:index"))

def delete_user(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home_page:login"))
    if request.method == "POST":
        user = get_user_model().objects.filter(username=request.user)
        user.delete()
        return render(request, DELETE_ACCOUNT_TEMPLATE)
    return render(request, DELETE_ACCOUNT_TEMPLATE, {"check_for_delete": True})
