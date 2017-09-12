from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    context = {
        'html_var':'f strings'
        
    }
    
    # return HttpResponse(html_) # another way to retun a response
    # return HttpResponse('Hello')
    return render(request, "base.html", context) # takes 3 args request, "template", {context}