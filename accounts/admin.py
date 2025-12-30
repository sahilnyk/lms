from django.contrib import admin
from .models import User, StudentProfile, TeacherProfile

class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "role", "organisation", "is_verified", "is_active", "created_at")
    search_fields = ("email", "name")
    list_filter = ("role", "organisation", "is_verified", "is_active")

admin.site.register(User, UserAdmin)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
