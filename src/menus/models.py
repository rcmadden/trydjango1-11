from django.conf import settings
from django.db import models

from restaurants.models import RestaurantLocation

# Create your models here.

class Item(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL)
    restaurant  = models.ForeignKey(RestaurantLocation)
    name         = models.CharField(max_length=120)
    contents    = models.TextField(help_text='Seperate each item by comma')
    excludes    = models.TextField(blank=True, null=True, help_text='Seperate each item by comma')
    public      = models.BooleanField(default=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated      = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated', '-timestamp'] # Item.objects.all() most recent updated item first
        
    def get_contents(self):
        return self.contents.split(",")
        
    def get_excludes(self):
        return self.excludes.split(",")
    