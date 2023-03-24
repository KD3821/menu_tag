from django.shortcuts import render
from django.views import View


class StartView(View):
    def get(self, request, key):
        menu_name = key
        return render(request, 'start.html', {'menu_name': menu_name})
