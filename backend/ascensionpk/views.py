from django.views.generic import View
from django.http import HttpResponse
import os

class FrontendAppView(View):
    def get(self, request):
        file_path = os.path.join(os.path.dirname(__file__), 'static', 'index.html')
        try:
            with open(file_path, 'r') as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return HttpResponse("React build not found", status=501)
