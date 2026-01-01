from django import forms
from tenancy.models import Organisation
from .models import User


class TenantSlugForm(forms.Form):
    slug = forms.CharField(max_length=50)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class OrganisationRegisterForm(forms.Form):
    org_name = forms.CharField(max_length=255, label="Organisation Name")
    slug = forms.SlugField(max_length=50, label="Organisation Slug")
    admin_name = forms.CharField(max_length=255, label="Admin Full Name")
    email = forms.EmailField(label="Admin Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Admin Password")
    org_address = forms.CharField(widget=forms.Textarea, label="Organisation Address")
    admin_address = forms.CharField(widget=forms.Textarea, label="Admin Address")
    org_size = forms.ChoiceField(
        choices=[
            ('', 'Select organisation size'),
            ('1-50', '1-50 users'),
            ('51-200', '51-200 users'),
            ('201-500', '201-500 users'),
            ('500+', '500+ users'),
        ],
        label="Organisation Size"
    )

    def clean_slug(self):
        slug = self.cleaned_data["slug"]
        if Organisation.objects.filter(slug=slug).exists():
            raise forms.ValidationError("Organisation slug already exists")
        return slug

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email


class SimpleUserForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email


class StudentRegisterForm(forms.Form):
    slug = forms.SlugField(max_length=50, label="Organisation Slug")
    name = forms.CharField(max_length=255, label="Full Name")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    phone = forms.CharField(max_length=20, label="Phone Number")
    address = forms.CharField(widget=forms.Textarea, label="Address")

    def clean_slug(self):
        slug = self.cleaned_data["slug"]
        if not Organisation.objects.filter(slug=slug, status="ACTIVE").exists():
            raise forms.ValidationError("Organisation not found or inactive")
        return slug

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email


class TeacherRegisterForm(forms.Form):
    slug = forms.SlugField(max_length=50, label="Organisation Slug")
    name = forms.CharField(max_length=255, label="Full Name")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    phone = forms.CharField(max_length=20, label="Phone Number")
    address = forms.CharField(widget=forms.Textarea, label="Address")

    def clean_slug(self):
        slug = self.cleaned_data["slug"]
        if not Organisation.objects.filter(slug=slug, status="ACTIVE").exists():
            raise forms.ValidationError("Organisation not found or inactive")
        return slug

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
