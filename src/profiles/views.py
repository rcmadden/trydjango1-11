from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, View

from menus.models import Item
from restaurants.models import RestaurantLocation


from .forms import RegisterForm
from .models import Profile
# Create your views here.


User = get_user_model()

def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = Profile.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.activated:
                user_ = profile.user
                user_.is_active = True
                user_.save()
                profile.ativated=True
                profile.activation_key=None
                profile.save()
                return redirect("/login")
    return redirect("/login")


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = '/'

    def dispatch(self, *args, **kwargs):
        # if self.request.user.is_authenticated():
        #     return redirect("/logout")
        return super(RegisterView, self).dispatch(*args, **kwargs)

class ProfileFollowToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # print(request.data)
        # print(request.POST)
        # user_to_toggle = request.POST.get("username")
        username_to_toggle = request.POST.get("username")
        profile_, is_following = Profile.objects.toggle_follow(request.user, username_to_toggle)

        print(is_following)
        # print(user_to_toggle)
        # move the logic below to models
        # profile_ = Profile.objects.get(user__username__iexact=user_to_toggle)
        # user = request.user
        # if user in profile_.followers.all():
        #     profile_.followers.remove(user)
        # else:
        #     profile_.followers.add(user)
            
        # return redirect("/u/russiam/")
        return redirect(f"/u/{profile_.user.username}/")
        

class ProfileDetailView(DetailView):
# returns user object for any given profile
    template_name = 'profiles/user.html'
    
    def get_object(self):
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(*args, **kwargs)
        # print(context)
        # user = self.get_object() # returns user twice not requested user
        user = context['user']
        is_following = False
        if user.profile in self.request.user.is_following.all():
            is_following = True
        context['is_following'] = is_following
        query = self.request.GET.get('q')
        items_exists = Item.objects.filter(user=user).exists()
        qs = RestaurantLocation.objects.filter(owner=user).search(query)
        # print(user.id)
        if items_exists and qs.exists():
            context['locations'] = qs
        return context