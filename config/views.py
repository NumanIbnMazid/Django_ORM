from django.views.generic import TemplateView, View
from django.shortcuts import render


class HomeView(TemplateView):
    template_name = 'home.html'
    
class ORM_VIEW(View):
    def get(self, request):
        return render(request, 'orm_view.html')