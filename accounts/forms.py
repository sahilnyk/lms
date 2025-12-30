from django import forms
from tenancy.models import Organisation
from .models import User


class TenantSlugForm(forms.Form):
    slug = forms.CharField(max_length=50)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class OrganisationRegisterForm(forms.Form):
    org_name = forms.CharField(max_length=255)
    slug = forms.SlugField(max_length=50)
    admin_name = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_slug(self):
        slug = self.cleaned_data["slug"]
        if Organisation.objects.filter(slug=slug).exists():
            raise forms.ValidationError("organisation slug already exists")
        return slug


class SimpleUserForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("email already exists")
        return email
