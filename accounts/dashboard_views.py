from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .permissions import role_required

@login_required
@role_required('ORG_ADMIN')
def admin_dashboard(request, slug):
    return render(request, 'accounts/admin_dashboard.html', {'slug': slug})

@login_required
@role_required('STUDENT')
def student_dashboard(request, slug):
    return render(request, 'accounts/student_dashboard.html', {'slug': slug})

@login_required
@role_required('TEACHER')
def teacher_dashboard(request, slug):
    return render(request, 'accounts/teacher_dashboard.html', {'slug': slug})