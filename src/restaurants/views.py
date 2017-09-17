from django.http import HttpResponse
from django.shortcuts import render
import random
from django.views import View
from django.views.generic import TemplateView


# Create your views here.
        
class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, *args, **kwargs):
        '''overiding method'''
        context = super(HomeView, self).get_context_data(*args, **kwargs)
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
        return context
        
        
class AboutView(TemplateView):
    template_name = 'about.html'
    
class MoreInfoView(TemplateView):
    template_name = 'more.info.html'

class ContactView(TemplateView):
    template_name = 'contact.html'
    
