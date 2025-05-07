from django.shortcuts import render
from django.http import HttpResponse

INDEX_TEMPLATE = "hours_tracker/index.html"

def index(request):
    return render(request, INDEX_TEMPLATE)
