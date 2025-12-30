from django.urls import path
from . import views

urlpatterns = [
    path('', views.platform_login_landing, name='platform_login_landing'),

    path('check-org/<slug:slug>/', views.check_org, name='check_org'),

    path('register/selector/', views.register_selector, name="register_selector"),
    path('register/organisation/', views.register_new_org, name="register_new_org"),

    path('<slug:slug>/login/', views.tenant_login_view, name='tenant_login'),
    path('<slug:slug>/register/org-admin/', views.register_org_admin, name='register_org_admin'),
    path('<slug:slug>/register/student/', views.register_student, name='register_student'),
    path('<slug:slug>/register/teacher/', views.register_teacher, name='register_teacher'),

    path('logout/', views.logout_view, name='logout'),
]
