from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout
from tenancy.models import Organisation
from .models import User, StudentProfile, TeacherProfile
from .forms import OrganisationRegisterForm, LoginForm, SimpleUserForm


def platform_login_landing(request):
    return render(request, "accounts/tenant_selector.html")


def check_org(request, slug):
    exists = Organisation.objects.filter(slug=slug, status="ACTIVE").exists()
    return JsonResponse({"exists": exists})


def get_org(slug):
    try:
        return Organisation.objects.get(slug=slug, status="ACTIVE")
    except Organisation.DoesNotExist:
        raise Http404("Organisation not found or suspended")


def tenant_login_view(request, slug):
    org = get_org(slug)
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        user = authenticate(request, username=email, password=password)

        if not user or user.organisation != org or not user.is_active:
            return render(request, "accounts/login.html", {
                "org": org,
                "form": form,
                "error": "invalid credentials"
            })

        if user.role == "TEACHER":
            t = TeacherProfile.objects.filter(user=user).first()
            if t and not t.approved:
                return render(request, "accounts/login.html", {
                    "org": org,
                    "form": form,
                    "error": "teacher approval pending"
                })

        login(request, user)

        if user.role == "ORG_ADMIN":
            return redirect(f"/{slug}/admin/dashboard/")
        if user.role == "TEACHER":
            return redirect(f"/{slug}/teacher/dashboard/")
        return redirect(f"/{slug}/student/dashboard/")

    return render(request, "accounts/login.html", {"org": org, "form": form})


def register_new_org(request):
    form = OrganisationRegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data

        org = Organisation.objects.create(
            name=data["org_name"],
            slug=data["slug"],
            status="ACTIVE"
        )

        User.objects.create_user(
            email=data["email"],
            password=data["password"],
            name=data["admin_name"],
            organisation=org,
            role="ORG_ADMIN",
            is_verified=True
        )

        return redirect("tenant_login", slug=data["slug"])

    return render(request, "accounts/register_new_org.html", {"form": form})


def register_org_admin(request, slug):
    org = get_org(slug)
    form = SimpleUserForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data

        User.objects.create_user(
            email=data["email"],
            password=data["password"],
            name=data["name"],
            organisation=org,
            role="ORG_ADMIN",
            is_verified=True
        )

        return redirect("tenant_login", slug=slug)

    return render(request, "accounts/register_org.html", {"org": org, "form": form})


def register_student(request, slug):
    org = get_org(slug)
    form = SimpleUserForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data

        user = User.objects.create_user(
            email=data["email"],
            password=data["password"],
            name=data["name"],
            organisation=org,
            role="STUDENT",
            is_verified=True
        )

        StudentProfile.objects.create(
            user=user,
            organisation=org
        )

        return redirect("tenant_login", slug=slug)

    return render(request, "accounts/register_student.html", {"org": org, "form": form})


def register_teacher(request, slug):
    org = get_org(slug)
    form = SimpleUserForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data

        user = User.objects.create_user(
            email=data["email"],
            password=data["password"],
            name=data["name"],
            organisation=org,
            role="TEACHER",
            is_verified=False
        )

        TeacherProfile.objects.create(
            user=user,
            organisation=org,
            approved=False
        )

        return redirect("tenant_login", slug=slug)

    return render(request, "accounts/register_teacher.html", {"org": org, "form": form})


def logout_view(request):
    logout(request)
    return redirect("/")
