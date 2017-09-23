from django import forms

# def RestaurantCreateForm(forms.Form): # why does this have to be a class?
class RestaurantCreateForm(forms.Form):
    name        = forms.CharField()
    location    = forms.CharField(required=False)
    category    = forms.CharField(required=False)