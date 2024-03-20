from django.urls import path, reverse_lazy
from . import views

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = "home_page"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("delete", views.delete_user, name="delete_account"),
    path("user/<str:user>", views.user_view, name="account"),
    path("change-password", views.change_password, name="change_password"),

    path("password-reset", PasswordResetView.as_view(template_name="home_page\password_reset.html", email_template_name="home_page\password_reset_email.html", success_url=reverse_lazy("home_page:password_reset_done")), name="password_reset"),

    path("password-reset-confirm/<uidb64>/<token>", PasswordResetConfirmView.as_view(template_name="home_page\password_reset_confirm.html", success_url=reverse_lazy("home_page:password_reset_complete")), name="password_reset_confirm"),

    path("password-reset/done", PasswordResetDoneView.as_view(template_name="home_page\password_reset_done.html"), name="password_reset_done"),

    path("password-reset-complete", PasswordResetCompleteView.as_view(template_name="home_page\password_reset_complete.html"), name="password_reset_complete")
]