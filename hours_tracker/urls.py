from django.urls import path

from . import views

app_name = "hours_tracker"
urlpatterns = [
    path("", views.index, name="index")
]