from django import forms
from .models import RestaurantLocation
from .validators import validate_category

# https://docs.djangoproject.com/en/1.11/ref/validators/
# def RestaurantCreateForm(forms.Form): # why does this have to be a class?
class RestaurantCreateForm(forms.Form):
    name        = forms.CharField()
    location    = forms.CharField(required=False)
    category    = forms.CharField(required=False)
    
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name == "Hello":
            raise forms.ValidationError("Not a valid name")
        return name
        
class RestaurantLocationCreateForm(forms.ModelForm):
    # email   = forms.EmailField() # or use #clean_email for more custom validation
    # category = forms.CharField(required= False, validators=[validate_category]) # add to model field itself
    class Meta:
        model = RestaurantLocation
        fields = [
            'name',
            'location',
            'category',
            ]
            
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name == "Hello":
            raise forms.ValidationError("Not a valid name")
        return name
        
    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if ".edu" in email:
    #         raise forms.ValidationError("We do not accept edu emails")
    #     return email
    