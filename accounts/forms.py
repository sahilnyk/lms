from django import forms
from tenancy.models import Organisation
from .models import User


VALID_ROLES = {"ORG_ADMIN", "TEACHER", "STUDENT"}


class RoleSelectionForm(forms.Form):
    ROLE_CHOICES = [
        ("ORG_ADMIN", "Organisation Admin"),
        ("TEACHER", "Teacher"),
        ("STUDENT", "Student"),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Select Your Role")

    def clean_role(self):
        role = self.cleaned_data["role"]
        if role not in VALID_ROLES:
            raise forms.ValidationError("Invalid role selected.")
        return role


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")


class OrganisationRegisterForm(forms.Form):
    org_name = forms.CharField(max_length=255, label="Organisation Name")
    slug = forms.SlugField(max_length=50, label="Organisation Slug")
    admin_name = forms.CharField(max_length=255, label="Full Name")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_slug(self):
        slug = self.cleaned_data["slug"].strip().lower()
        if Organisation.objects.filter(slug=slug).exists():
            raise forms.ValidationError("Organisation slug already exists.")
        return slug

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class TeacherRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100, label="Last Name")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    organisation_slug = forms.SlugField(max_length=50, label="Organisation Slug")
    phone = forms.CharField(max_length=20, label="Phone Number")
    address = forms.CharField(widget=forms.Textarea, required=False, label="Address")

    def clean_organisation_slug(self):
        slug = self.cleaned_data["organisation_slug"].strip().lower()
        if not Organisation.objects.filter(slug=slug, status="ACTIVE").exists():
            raise forms.ValidationError("Organisation not found or inactive.")
        return slug

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class StudentRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100, label="Last Name")
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    organisation_slug = forms.SlugField(max_length=50, label="Organisation Slug")
    phone = forms.CharField(max_length=20, label="Phone Number")
    address = forms.CharField(widget=forms.Textarea, required=False, label="Address")

    def clean_organisation_slug(self):
        slug = self.cleaned_data["organisation_slug"].strip().lower()
        if not Organisation.objects.filter(slug=slug, status="ACTIVE").exists():
            raise forms.ValidationError("Organisation not found or inactive.")
        return slug

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
