from django.db import models
from django.db.models.signals import pre_save, post_save

from .utils import unique_slug_generator

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


# two ways of saving using signals pre or post with passing then saving the instance       
def rl_pre_save_receiver(sender, instance, *args, **kwargs):
     print('saving ... ')
     print(instance.timestamp)
     # if not instance.slug:
     #      instance.name = 'Another New Name'
     #      instance.slug = unique_slug_generator(instance)
          
def rl_post_save_receiver(sender, instance, created, *args, **kwargs):
     print('saved')
     print(instance.timestamp)
     if not instance.slug:
          instance.slug = unique_slug_generator(instance)
          instance.save()
          
pre_save.connect(rl_pre_save_receiver, sender=RestaurantLocation)
     
post_save.connect(rl_post_save_receiver, sender=RestaurantLocation)