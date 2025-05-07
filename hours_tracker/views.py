from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
import json

INDEX_TEMPLATE = "hours_tracker/index.html"

class IndexView(View):

    def get(self, request):
        return render(request, INDEX_TEMPLATE)

    def post(self, request):

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")
        
        # check which form was sent

        return render(request, INDEX_TEMPLATE)
