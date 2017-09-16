from django.http import HttpResponse
from django.shortcuts import render
import random
from django.views import View


# Create your views here.
def home(request):
    bool_item = True
    num = None
    some_list = (random.randint(0, 10000), random.randint(0, 10000), random.randint(0, 10000))
    # logic in view instead of template
    if bool_item:
        num = random.randint(0, 10000000)
        
    context = {
        'bool_item': bool_item,
        'html_var':'f strings',
        'num': num,
        'some_list': some_list
    }
    
    return render(request, "home.html", context) # takes 3 args request, "template", {context}
    
def about(request):
    context = {}
    return render(request, "about.html", context) 
    
def contact(request):
    context = {}
    return render(request, "contact.html", context) 


def moreinfo(request):
    context = {}
    return render(request, "more.info.html", context) 
    
class ConactView(View):
    def get(self, request, *args, **kwargs):
        return