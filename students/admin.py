from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Student

@admin.register(Student)
class StudentAdmin(SimpleHistoryAdmin):
    list_display = (
        'roll_number', 'first_name', 'last_name', 'academic_year', 'degree_type', 'admission_date'
    )
    search_fields = ('first_name', 'last_name', 'roll_number')
    list_filter = ('academic_year', 'degree_type', 'state', 'city')
