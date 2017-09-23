from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from .forms import RestaurantCreateForm
from .models import RestaurantLocation


# Create your views here.
def restaurant_createview(request):
    form = RestaurantCreateForm(request.POST or None)
    errors = None
    # if request.method == 'POST':
        # title    = request.POST.get('title')
        # location = request.POST.get('location')
        # category = request.POST.get('category')
        # form = RestaurantCreateForm(request.POST)
    if form.is_valid():
        obj = RestaurantLocation.objects.create(
        name=form.cleaned_data.get('name'),
        location=form.cleaned_data.get('location'),
        category=form.cleaned_data.get('category')
        )
        return HttpResponseRedirect("/restaurants/")
    if form.errors:
        # print(form.errors)
        errors = form.errors
    template_name = 'restaurants/form.html'
    context = {"form": form, "errors": errors}
    return render(request, template_name, context)


def restaruant_listview(request):
    template_name = 'restaurants/restaruants_list.html'
    queryset = RestaurantLocation.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request, template_name, context)

def restaruant_detailview(request, slug):
    template_name = 'restaurants/restauranlocation_detail.html'
    obj = RestaurantLocation.objects.get(slug=slug)
    context = {
        "object": obj
    }
    return render(request, template_name, context)


class RestaurantListView(ListView):
    def get_queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            queryset = RestaurantLocation.objects.filter(
                Q(category__iexact=slug) |
                Q(category__icontains=slug) 
                )
        else:
            queryset = RestaurantLocation.objects.all()
        return queryset
    
class RestaurantDetailView(DetailView):
    # queryset = RestaurantLocation.objects.filter(category__contains='asian') # will use to filter by user
    queryset = RestaurantLocation.objects.all()
    # def get_context_data(self, *args, **kwargs):
    #     print(self.kwargs)
    #     context = super(RestaurantDetailView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context
    
    # def get_object(self, *args, **kwargs):
    #     rest_id = self.kwargs.get('rest_id')
    #     obj = get_object_or_404(RestaurantLocation, id=rest_id)
    #     return obj
