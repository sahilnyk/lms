from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Student

@admin.register(Student)
class StudentAdmin(SimpleHistoryAdmin):
    fieldsets = (
        ('👤 Student Name', {
            'fields': (('first_name', 'last_name'),),
        }),
        ('🏠 Address', {
            'fields': (('street_name', 'area'), ('city', 'state', 'pin_code')),
        }),
        ('👪 Parent Details', {
            'fields': (('father_name', 'mother_name'), ('parent_contact_number', 'parent_email')),
        }),
        ('🎓 Academic Info', {
            'fields': (('admission_date', 'academic_year', 'degree_type', 'roll_number'),),
        }),
    )
    readonly_fields = ('roll_number', 'admission_date')
    list_display = ('roll_number', 'first_name', 'last_name', 'academic_year', 'degree_type', 'admission_date')
    search_fields = ('first_name', 'last_name', 'roll_number')
    list_filter = ('academic_year', 'degree_type', 'state', 'city')
