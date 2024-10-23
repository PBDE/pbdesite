from django.shortcuts import render

INDEX_TEMPLATE = "legion/index.html"

def index(request):
    return render(request, INDEX_TEMPLATE)