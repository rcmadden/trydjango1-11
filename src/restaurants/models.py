from django.db import models

# Create your models here.
class RestaurantLocation(models.Model):
     name       = models.CharField(max_length=120)
     location   = models.CharField(max_length=120, null=True, blank=True)
     category   = models.CharField(max_length=120, null=True, blank=True)
     timestamp  = models.DateTimeField(auto_now=True)
     updated    = models.DateTimeField(auto_now=True)
     # slug       = models.SlugField(unique=True)
     slug       = models.SlugField(null=True, blank=True)
     
     
     # replaces object name in django admin with field name
     def __str__(self):
         return self.name
     
     @property
     def title(self):
          return self.name  # so we can use obj.title
          