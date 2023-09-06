from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .home_page_forms import LoginForm, CreateUser


def index(request):
    return render(request, "home_page/index.html")


def register(request):
    if request.method == "POST":
        new_user_form = CreateUser(request.POST)
        if new_user_form.is_valid():
            user = User.objects.create_user(new_user_form.cleaned_data["username"], 
                                            new_user_form.cleaned_data["email"], 
                                            new_user_form.cleaned_data["password1"])
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("home_page:account"))
        else:
            return render(request, "home_page/register.html", {
                "form": new_user_form
            })
    return render(request, "home_page/register.html", {
        "form": CreateUser()
    })


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home_page:account', kwargs={"user": request.user.username}))
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse("home_page:account", kwargs={"user": username}))
            else:
                return render(request, "home_page/login.html", {
                "form": login_form,
                "message": "Details did not match an existing user"
            })
        else:
            return render(request, "home_page/login.html", {
                "form": login_form,
                "message": "Invalid login details"
            })
    return render(request, "home_page/login.html", {
        "form": LoginForm()
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home_page:login"))


def user_view(request, user):

    print("User:", user)

    if request.user.is_authenticated and user == request.user.username:
        return render(request, f"home_page/account.html")
    elif User.objects.filter(username=user).exists():
        return HttpResponseRedirect(reverse("home_page:login"))
    else:
        return HttpResponseRedirect(reverse("home_page:index"))


def delete_user(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home_page:login"))
    if request.method == "POST":
        user = User.objects.filter(username=request.user)
        user.delete()
        return render(request, "home_page/delete_account.html", {"delete_account": True})
    return render(request, "home_page/delete_account.html")
