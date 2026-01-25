from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from tenancy.models import Organisation
from .models import User, StudentProfile, TeacherProfile
from .forms import (
    LoginForm,
    OrganisationRegisterForm,
    StudentRegisterForm,
    TeacherRegisterForm
)
from .serializers import CustomTokenObtainPairSerializer
from .api_permission import IsTenantUser, AllowTokenObtain


VALID_ROLES = {"ORG_ADMIN", "TEACHER", "STUDENT"}

ROLE_LOGIN_ROUTES = {
    "ORG_ADMIN": "login_admin",
    "TEACHER": "login_teacher",
    "STUDENT": "login_student",
}

ROLE_REGISTER_ROUTES = {
    "ORG_ADMIN": "register_admin",
    "TEACHER": "register_teacher",
    "STUDENT": "register_student",
}

ROLE_DASHBOARD_ROUTES = {
    "ORG_ADMIN": "admin_dashboard",
    "TEACHER": "teacher_dashboard",
    "STUDENT": "student_dashboard",
}

class TenantTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowTokenObtain]

    def post(self, request, *args, **kwargs):
        org_id = request.data.get("organisation_id")
        if not org_id:
            return Response(
                {"detail": "organisation_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response(
                {
                    "refresh": response.data.get("refresh"),
                    "access": response.data.get("access")
                },
                status=200
            )
        return response


class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = [AllowAny, IsTenantUser]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            RefreshToken(refresh_token).blacklist()
            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception:
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST
            )

def check_org(request, slug):
    exists = Organisation.objects.filter(slug=slug, status="ACTIVE").exists()
    return JsonResponse({"exists": exists})


def _clear_login_session(request):
    request.session.pop("login_org_slug", None)
    request.session.pop("login_role", None)


def _get_login_org(request):
    slug = request.session.get("login_org_slug")
    if not slug:
        return None, None

    try:
        org = Organisation.objects.get(slug=slug, status="ACTIVE")
        return slug, org
    except Organisation.DoesNotExist:
        return slug, None

def platform_login_landing(request):
    return render(request, "accounts/login/login_slug.html")


def login_slug_view(request):
    if request.method == "POST":
        slug = request.POST.get("slug", "").strip().lower()

        if not slug:
            messages.error(request, "Organisation slug is required.")
            return redirect("login_slug")

        if not Organisation.objects.filter(slug=slug, status="ACTIVE").exists():
            messages.error(request, "Organisation not found or inactive.")
            return redirect("login_slug")

        request.session["login_org_slug"] = slug
        return redirect("login_selector")

    return render(request, "accounts/login/login_slug.html")


def login_selector_view(request):
    if not request.session.get("login_org_slug"):
        messages.error(request, "Please enter your organisation first.")
        return redirect("login_slug")

    if request.method == "POST":
        role = request.POST.get("role", "").strip().upper()
        if role not in VALID_ROLES:
            messages.error(request, "Please select a valid role.")
            return render(request, "accounts/login/login_selector.html")

        request.session["login_role"] = role
        return redirect(ROLE_LOGIN_ROUTES[role])

    return render(request, "accounts/login/login_selector.html")


def login_admin_view(request):
    slug, org = _get_login_org(request)
    if not slug or not org:
        _clear_login_session(request)
        return redirect("login_slug")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["email"],
            password=form.cleaned_data["password"]
        )

        if not user or user.organisation != org or user.role != "ORG_ADMIN" or not user.is_active:
            messages.error(request, "Invalid credentials.")
            return render(request, "accounts/login/login_admin.html", {"form": form, "org": org})

        login(request, user)
        _clear_login_session(request)
        return redirect(ROLE_DASHBOARD_ROUTES["ORG_ADMIN"], slug=slug)

    return render(request, "accounts/login/login_admin.html", {"form": form, "org": org})


def login_teacher_view(request):
    slug, org = _get_login_org(request)
    if not slug or not org:
        _clear_login_session(request)
        return redirect("login_slug")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["email"],
            password=form.cleaned_data["password"]
        )

        if not user or user.organisation != org or user.role != "TEACHER" or not user.is_active:
            messages.error(request, "Invalid credentials.")
            return render(request, "accounts/login/login_teacher.html", {"form": form, "org": org})

        profile = TeacherProfile.objects.filter(user=user).first()
        if not profile or not profile.approved:
            messages.error(request, "Your account is pending admin approval.")
            return render(request, "accounts/login/login_teacher.html", {"form": form, "org": org})

        login(request, user)
        _clear_login_session(request)
        return redirect(ROLE_DASHBOARD_ROUTES["TEACHER"], slug=slug)

    return render(request, "accounts/login/login_teacher.html", {"form": form, "org": org})


def login_student_view(request):
    slug, org = _get_login_org(request)
    if not slug or not org:
        _clear_login_session(request)
        return redirect("login_slug")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["email"],
            password=form.cleaned_data["password"]
        )

        if not user or user.organisation != org or user.role != "STUDENT" or not user.is_active:
            messages.error(request, "Invalid credentials.")
            return render(request, "accounts/login/login_student.html", {"form": form, "org": org})

        login(request, user)
        _clear_login_session(request)
        return redirect(ROLE_DASHBOARD_ROUTES["STUDENT"], slug=slug)

    return render(request, "accounts/login/login_student.html", {"form": form, "org": org})

def register_selector(request):
    if request.method == "POST":
        role = request.POST.get("role", "").strip().upper()
        if role not in VALID_ROLES:
            messages.error(request, "Please select a valid role.")
            return render(request, "accounts/register/register_selector.html")

        request.session["register_role"] = role
        return redirect(ROLE_REGISTER_ROUTES[role])

    return render(request, "accounts/register/register_selector.html")


def register_admin(request):
    if request.session.get("register_role") != "ORG_ADMIN":
        messages.error(request, "Invalid registration flow.")
        return redirect("register_selector")

    form = OrganisationRegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data

        if Organisation.objects.filter(slug=data["slug"]).exists():
            form.add_error("slug", "This organisation slug is already taken.")
            return render(request, "accounts/register/register_admin.html", {"form": form})

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

        request.session.pop("register_role", None)
        messages.success(request, "Organisation created successfully. Please login.")
        return redirect("login_slug")

    return render(request, "accounts/register/register_admin.html", {"form": form})


def register_teacher(request):
    if request.session.get("register_role") != "TEACHER":
        messages.error(request, "Invalid registration flow.")
        return redirect("register_selector")

    form = TeacherRegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data

        try:
            org = Organisation.objects.get(slug=data["organisation_slug"], status="ACTIVE")
        except Organisation.DoesNotExist:
            form.add_error("organisation_slug", "Organisation not found or inactive.")
            return render(request, "accounts/register/register_teacher.html", {"form": form})

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

        TeacherProfile.objects.create(user=user, organisation=org, approved=False)

        request.session.pop("register_role", None)
        messages.success(request, "Registration successful. Awaiting admin approval.")
        return redirect("login_slug")

    return render(request, "accounts/register/register_teacher.html", {"form": form})


def register_student(request):
    if request.session.get("register_role") != "STUDENT":
        messages.error(request, "Invalid registration flow.")
        return redirect("register_selector")

    form = StudentRegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data

        try:
            org = Organisation.objects.get(slug=data["organisation_slug"], status="ACTIVE")
        except Organisation.DoesNotExist:
            form.add_error("organisation_slug", "Organisation not found or inactive.")
            return render(request, "accounts/register/register_student.html", {"form": form})

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

        StudentProfile.objects.create(user=user, organisation=org)

        request.session.pop("register_role", None)
        messages.success(request, "Registration successful. Please login.")
        return redirect("login_slug")

    return render(request, "accounts/register/register_student.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login_slug")


def admin_dashboard(request, slug):
    if not request.user.is_authenticated or request.user.role != "ORG_ADMIN":
        return redirect("login_slug")
    if request.user.organisation.slug != slug:
        return redirect("login_slug")
    return render(request, "accounts/admin_dashboard.html", {"slug": slug})


def teacher_dashboard(request, slug):
    if not request.user.is_authenticated or request.user.role != "TEACHER":
        return redirect("login_slug")
    if request.user.organisation.slug != slug:
        return redirect("login_slug")
    return render(request, "accounts/teacher_dashboard.html", {"slug": slug})


def student_dashboard(request, slug):
    if not request.user.is_authenticated or request.user.role != "STUDENT":
        return redirect("login_slug")
    if request.user.organisation.slug != slug:
        return redirect("login_slug")
    return render(request, "accounts/student_dashboard.html", {"slug": slug})
