from django.urls import path
from . import views

urlpatterns = [
    path('', views.platform_login_landing, name='platform_login_landing'),
    path('check-org/<slug:slug>/', views.check_org, name='check_org'),
    path('<slug:slug>/role/', views.tenant_role_selection, name='tenant_role_selection'),
    path('<slug:slug>/login/', views.tenant_login_view, name='tenant_login'),    
    path('register/', views.register_selector, name='register_selector'),
    path('register/slug/', views.register_step_slug, name='register_step_slug'),
    path('register/organisation/', views.register_new_org, name='register_new_org'),
    path('register/student/', views.register_student_public, name='register_student_public'),
    path('register/teacher/', views.register_teacher_public, name='register_teacher_public'),
    path('logout/', views.logout_view, name='logout'),
    path('<slug:slug>/admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('<slug:slug>/student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('<slug:slug>/teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
]
