from django.http import HttpResponse
from django.shortcuts import render
import random

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
    
    # return HttpResponse(html_) # another way to retun a response
    # return HttpResponse('Hello')
    return render(request, "base.html", context) # takes 3 args request, "template", {context}