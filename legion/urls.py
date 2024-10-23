from django.urls import path

from . import views

app_name = "legion"
urlpatterns = [
    path("", views.index, name="index")
]