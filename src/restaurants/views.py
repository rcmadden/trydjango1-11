from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView

from .models import RestaurantLocation

# Create your views here.
def restaruant_listview(request):
    template_name = 'restaurants/restaruants_list.html'
    queryset = RestaurantLocation.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request, template_name, context)

class RestaurantListView(ListView):
    queryset = RestaurantLocation.objects.all()
    template_name = 'restaurants/restaruants_list.html'

    
class MexianRestaurantListView(ListView):
    queryset = RestaurantLocation.objects.filter(category__iexact='mexican')
    template_name = 'restaurants/restaruants_list.html'

class AsianFusionRestaurantListView(ListView):
    queryset = RestaurantLocation.objects.filter(category__iexact='asian fusion')
    template_name = 'restaurants/restaruants_list.html'
    
