from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path("", views.platform_login_landing, name="platform_login_landing"),
    path("check-org/<slug:slug>/", views.check_org, name="check_org"),
    path("login/slug/", views.login_slug_view, name="login_slug"),
    path("login/selector/", views.login_selector_view, name="login_selector"),
    path("login/admin/", views.login_admin_view, name="login_admin"),
    path("login/teacher/", views.login_teacher_view, name="login_teacher"),
    path("login/student/", views.login_student_view, name="login_student"),
    path("register/", views.register_selector, name="register_selector"),
    path("register/admin/", views.register_admin, name="register_admin"),
    path("register/teacher/", views.register_teacher, name="register_teacher"),
    path("register/student/", views.register_student, name="register_student"),
    path("logout/", views.logout_view, name="logout"),
    path("<slug:slug>/admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("<slug:slug>/teacher/dashboard/", views.teacher_dashboard, name="teacher_dashboard"),
    path("<slug:slug>/student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("api/token/", views.TenantTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/logout/", views.LogoutAndBlacklistRefreshTokenForUserView.as_view(), name="token_logout"),
]
