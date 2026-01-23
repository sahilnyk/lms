from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from tenancy.models import Organisation
from .models import User, StudentProfile, TeacherProfile
from .forms import (
    OrganisationSlugForm,
    RoleSelectionForm,
    LoginForm,
    OrganisationRegisterForm,
    StudentRegisterForm,
    TeacherRegisterForm
)
from .serializers import CustomTokenObtainPairSerializer
from .api_permission import IsTenantUser

# --- JWT API VIEWS ---
class TenantTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        org_id = request.data.get('organisation_id')
        if not org_id:
            return Response({'detail': 'organisation_id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        # Optionally, you can add more org/user validation here
        response = super().post(request, *args, **kwargs)
        # Only return allowed fields
        if response.status_code == 200:
            data = response.data
            allowed = {'refresh', 'access'}
            filtered = {k: v for k, v in data.items() if k in allowed}
            return Response(filtered, status=200)
        return response

class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail': 'Refresh token required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        
def platform_login_landing(request):
    return render(request, "accounts/tenant_selector.html")


def check_org(request, slug):
    exists = Organisation.objects.filter(slug=slug, status="ACTIVE").exists()
    return JsonResponse({"exists": exists})


def tenant_role_selection(request, slug):
    try:
        org = Organisation.objects.get(slug=slug, status="ACTIVE")
    except Organisation.DoesNotExist:
        messages.error(request, "Organisation not found")
        return redirect('platform_login_landing')
    
    request.session['login_org_slug'] = slug
    
    if request.method == "POST":
        role = request.POST.get('role')
        if role in ['ORG_ADMIN', 'TEACHER', 'STUDENT']:
            request.session['login_role'] = role
            return redirect('tenant_login', slug=slug)
    
    return render(request, "accounts/role_selector.html", {"org": org})


def tenant_login_view(request, slug):
    login_slug = request.session.get('login_org_slug')
    login_role = request.session.get('login_role')
    
    if not login_slug or login_slug != slug or not login_role:
        return redirect('tenant_role_selection', slug=slug)
    
    try:
        org = Organisation.objects.get(slug=slug, status="ACTIVE")
    except Organisation.DoesNotExist:
        messages.error(request, "Organisation not found")
        return redirect('platform_login_landing')
    
    form = LoginForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        
        user = authenticate(request, username=email, password=password)
        
        if not user:
            messages.error(request, "Invalid email or password")
            return render(request, "accounts/login.html", {
                "org": org,
                "role": login_role,
                "form": form
            })
        
        if user.organisation != org:
            messages.error(request, "You are not registered with this organisation")
            return render(request, "accounts/login.html", {
                "org": org,
                "role": login_role,
                "form": form
            })
        
        if user.role != login_role:
            messages.error(request, f"Your account is registered as {user.get_role_display()}, not {dict(User.ROLE_CHOICES).get(login_role)}")
            return render(request, "accounts/login.html", {
                "org": org,
                "role": login_role,
                "form": form
            })
        
        if not user.is_active:
            messages.error(request, "Your account has been deactivated")
            return render(request, "accounts/login.html", {
                "org": org,
                "role": login_role,
                "form": form
            })
        
        if user.role == "TEACHER":
            try:
                teacher_profile = TeacherProfile.objects.get(user=user)
                if not teacher_profile.approved:
                    messages.error(request, "Your teacher account is pending approval from the organisation admin")
                    return render(request, "accounts/login.html", {
                        "org": org,
                        "role": login_role,
                        "form": form
                    })
            except TeacherProfile.DoesNotExist:
                messages.error(request, "Teacher profile not found")
                return render(request, "accounts/login.html", {
                    "org": org,
                    "role": login_role,
                    "form": form
                })
        
        login(request, user)
        
        request.session.pop('login_org_slug', None)
        request.session.pop('login_role', None)
        
        if user.role == "ORG_ADMIN":
            return redirect('admin_dashboard', slug=slug)
        elif user.role == "TEACHER":
            return redirect('teacher_dashboard', slug=slug)
        elif user.role == "STUDENT":
            return redirect('student_dashboard', slug=slug)
    
    return render(request, "accounts/login.html", {
        "org": org,
        "role": login_role,
        "form": form
    })


def register_selector(request):
    if request.method == "POST":
        role = request.POST.get('role')
        if role in ['ORG_ADMIN', 'TEACHER', 'STUDENT']:
            request.session['register_role'] = role
            return redirect('register_step_slug')
    
    return render(request, "accounts/register_selector.html")


def register_step_slug(request):
    role = request.session.get('register_role')
    
    if not role:
        return redirect('register_selector')
    
    if request.method == "POST":
        slug = request.POST.get('slug', '').strip()
        
        if not slug:
            messages.error(request, "Organisation slug is required")
            return render(request, "accounts/register_slug.html", {"role": role})
        
        org_exists = Organisation.objects.filter(slug=slug).exists()
        
        if role == 'ORG_ADMIN':
            if org_exists:
                messages.error(request, "Organisation slug already exists. Please choose a different slug")
                return render(request, "accounts/register_slug.html", {"role": role})
            request.session['register_slug'] = slug
            return redirect('register_new_org')
        else:
            if not org_exists:
                messages.error(request, "Organisation not found. Please contact your organisation admin")
                return render(request, "accounts/register_slug.html", {"role": role})
            
            try:
                org = Organisation.objects.get(slug=slug, status="ACTIVE")
                request.session['register_slug'] = slug
                
                if role == 'STUDENT':
                    return redirect('register_student_public')
                elif role == 'TEACHER':
                    return redirect('register_teacher_public')
            except Organisation.DoesNotExist:
                messages.error(request, "Organisation is not active")
                return render(request, "accounts/register_slug.html", {"role": role})
    
    return render(request, "accounts/register_slug.html", {"role": role})


def register_new_org(request):
    role = request.session.get('register_role')
    slug_session = request.session.get('register_slug')
    
    if role != 'ORG_ADMIN' or not slug_session:
        return redirect('register_selector')
    
    form = OrganisationRegisterForm(request.POST or None, initial={'slug': slug_session})
    
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        
        org = Organisation.objects.create(
            name=data["org_name"],
            slug=data["slug"],
            status="ACTIVE",
            address=data["org_address"],
            size=data["org_size"]
        )
        
        User.objects.create_user(
            email=data["email"],
            password=data["password"],
            name=data["admin_name"],
            organisation=org,
            role="ORG_ADMIN",
            is_verified=True,
            address=data["admin_address"]
        )
        
        request.session.pop('register_role', None)
        request.session.pop('register_slug', None)
        
        messages.success(request, "Organisation created successfully! You can now login")
        return redirect('platform_login_landing')
    
    return render(request, "accounts/register_new_org.html", {"form": form})


def register_student_public(request):
    role = request.session.get('register_role')
    slug = request.session.get('register_slug')
    
    if role != 'STUDENT' or not slug:
        return redirect('register_selector')
    
    try:
        org = Organisation.objects.get(slug=slug, status="ACTIVE")
    except Organisation.DoesNotExist:
        messages.error(request, "Organisation not found")
        return redirect('register_selector')
    
    form = StudentRegisterForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        
        user = User.objects.create_user(
            email=data["email"],
            password=data["password"],
            name=f"{data['first_name']} {data['last_name']}",
            organisation=org,
            role="STUDENT",
            is_verified=True,
            phone=data["phone"],
            address=data["address"]
        )
        
        StudentProfile.objects.create(
            user=user,
            organisation=org
        )
        
        request.session.pop('register_role', None)
        request.session.pop('register_slug', None)
        
        messages.success(request, "Student account created successfully! You can now login")
        return redirect('platform_login_landing')
    
    return render(request, "accounts/register_student_public.html", {
        "form": form,
        "org": org
    })


def register_teacher_public(request):
    role = request.session.get('register_role')
    slug = request.session.get('register_slug')
    
    if role != 'TEACHER' or not slug:
        return redirect('register_selector')
    
    try:
        org = Organisation.objects.get(slug=slug, status="ACTIVE")
    except Organisation.DoesNotExist:
        messages.error(request, "Organisation not found")
        return redirect('register_selector')
    
    form = TeacherRegisterForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        
        user = User.objects.create_user(
            email=data["email"],
            password=data["password"],
            name=f"{data['first_name']} {data['last_name']}",
            organisation=org,
            role="TEACHER",
            is_verified=False,
            phone=data["phone"],
            address=data["address"]
        )
        
        TeacherProfile.objects.create(
            user=user,
            organisation=org,
            approved=False
        )
        
        request.session.pop('register_role', None)
        request.session.pop('register_slug', None)
        
        messages.success(request, "Teacher account created successfully! Your account is pending approval from the organisation admin")
        return redirect('platform_login_landing')
    
    return render(request, "accounts/register_teacher_public.html", {
        "form": form,
        "org": org
    })


def logout_view(request):
    logout(request)
    return redirect('platform_login_landing')


def admin_dashboard(request, slug):
    if not request.user.is_authenticated or request.user.role != 'ORG_ADMIN':
        return redirect('platform_login_landing')
    return render(request, "accounts/admin_dashboard.html", {"slug": slug})


def student_dashboard(request, slug):
    if not request.user.is_authenticated or request.user.role != 'STUDENT':
        return redirect('platform_login_landing')
    return render(request, "accounts/student_dashboard.html", {"slug": slug})


def teacher_dashboard(request, slug):
    if not request.user.is_authenticated or request.user.role != 'TEACHER':
        return redirect('platform_login_landing')
    return render(request, "accounts/teacher_dashboard.html", {"slug": slug})
