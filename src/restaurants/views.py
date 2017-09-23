from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .forms import RestaurantCreateForm, RestaurantLocationCreateForm
from .models import RestaurantLocation

# FunctionBasedViews - django login_required decorator https://docs.djangoproject.com/en/1.11/topics/auth/default/#django.contrib.auth.decorators.login_required
# ClassBasedViews - django login_required mixins  https://docs.djangoproject.com/en/1.11/topics/auth/default/#the-loginrequired-mixin

# Create your views here.
@login_required()
def restaurant_createview(request):
    form = RestaurantLocationCreateForm(request.POST or None)
    errors = None
    if form.is_valid():
        if request.user.is_authenticated():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            return HttpResponseRedirect("/restaurants/")
        else:
            return HttpResponseRedirect("/login/")
    if form.errors:
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
    queryset = RestaurantLocation.objects.all()


class RestaurantCreateView(LoginRequiredMixin, CreateView):
    form_class = RestaurantLocationCreateForm
    # login_url = '/login/' # or in the decorator
    template_name = 'restaurants/form.html'
    success_url = "/restaurants/"
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        # instance.save() #Django CreateView does the call to instance.save() by default
        return super(RestaurantCreateView, self).form_valid(form)
    