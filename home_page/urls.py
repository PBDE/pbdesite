from django.urls import path
from . import views

app_name = "home_page"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("delete", views.delete_user, name="delete_account"),
    path("<str:user>", views.user_view, name="account"),
]