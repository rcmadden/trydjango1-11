from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse

from .utils import unique_slug_generator
from .validators import validate_category

# foreign keys: https://docs.djangoproject.com/en/1.11/ref/models/fields/#foreignkey
# user models: https://docs.djangoproject.com/en/1.11/ref/contrib/auth/

User = settings.AUTH_USER_MODEL
#RestaurantLocation.objects.all().search(query) or (something).search

class ProfileManager(models.Manager):
     def toggle_follow(self, request_user, username_to_toggle):
          profile_ = Profile.objects.get(user__username__iexact=username_to_toggle)
          user = request_user
          is_following = False
          if user in profile_.followers.all():
               profile_.followers.remove(user)
          else:
               profile_.followers.add(user)
               is_following = True
          return profile_, is_following
     
     
class RestaurantLocationQuerySet(models.query.QuerySet):
     def search(self, query):
          if query:
               query = query.strip()
               return self.filter(
                  Q(name__icontains=query)|
                  Q(location__icontains=query)|   
                  Q(location__iexact=query)|
                  Q(category__icontains=query)|
                  Q(category__iexact=query)|
                  Q(item__name__icontains=query)|
                  Q(item__contents__icontains=query)
                  ).distinct()
          return self

class RestaurantLocationManager(models.Manager):
     def get_queryset(self):
          return RestaurantLocationQuerySet(self.model, using=self._db)
          
     def search(self, query): #RestaurantLocation.objects.search()
        return self.get_queryset().search(query)
        

# Create your models here.
class RestaurantLocation(models.Model):
     owner      = models.ForeignKey(User) # class_instance.model_set.all() #Django Models Unleashed to understand how these work
     name       = models.CharField(max_length=120)
     location   = models.CharField(max_length=120, null=True, blank=True)
     category   = models.CharField(max_length=120, null=True, blank=True, validators=[validate_category])
     timestamp  = models.DateTimeField(auto_now=True)
     updated    = models.DateTimeField(auto_now=True)
     # slug       = models.SlugField(unique=True)
     slug       = models.SlugField(null=True, blank=True)
      
     objects = RestaurantLocationManager() # add Model.objects.all() to model
     
     # replaces object name in django admin with field name
     def __str__(self):
         return self.name
     
     def get_absolute_url(self):
          return reverse('restaurants:detail', kwargs={'slug':self.slug})
     
     @property
     def title(self):
          return self.name  # so we can use obj.title


# two ways of saving using signals pre or post with passing then saving the instance       
def rl_pre_save_receiver(sender, instance, *args, **kwargs):
     instance.category = instance.category.capitalize()
     if not instance.slug:
          instance.slug = unique_slug_generator(instance)
          
# def rl_post_save_receiver(sender, instance, created, *args, **kwargs):
#      print('saved')
#      print(instance.timestamp)
#      if not instance.slug:
#           instance.slug = unique_slug_generator(instance)
#           instance.save()
          
pre_save.connect(rl_pre_save_receiver, sender=RestaurantLocation)
     
# post_save.connect(rl_post_save_receiver, sender=RestaurantLocation)