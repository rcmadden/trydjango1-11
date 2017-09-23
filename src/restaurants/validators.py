from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _

# source: https://docs.djangoproject.com/en/1.11/ref/validators/

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            '%(value)s is not an even number',
            # _('%(value)s is not an even number'),
            params={'value': value},
        )

def clean_email(value):
        email = value
        if ".edu" in email:
            raise forms.ValidationError("We do not accept edu emails")

CATEGORIES = ['Mexican', 'Asian', 'America', 'Breakfast']

def validate_category(value):
    cat = value.capitalize()
    if not value in CATEGORIES and not cat in CATEGORIES:
        raise ValidationError(f"{value} not a valid category")
    return cat