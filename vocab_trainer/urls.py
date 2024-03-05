from django.urls import path
from . import views

app_name = "vocab_trainer"
urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("test", views.test, name="test"),
    path("translations", views.translations_table, name="translations")
]