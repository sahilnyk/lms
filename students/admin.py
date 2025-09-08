from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Student, Address, ParentGuardian

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street_name', 'area', 'city', 'state', 'country', 'pin_code', 'address_type')
    search_fields = ('city', 'state', 'country')

@admin.register(ParentGuardian)
class ParentGuardianAdmin(admin.ModelAdmin):
    list_display = ('name', 'relationship', 'phone', 'email', 'occupation')
    search_fields = ('name', 'relationship', 'phone')

@admin.register(Student)
class StudentAdmin(SimpleHistoryAdmin):
    fieldsets = (
        ('👤 Student Info', {
            'fields': (('first_name', 'middle_name', 'last_name'), ('date_of_birth', 'gender', 'photograph')),
        }),
        ('📞 Contact', {
            'fields': (('phone', 'email'),),
        }),
        ('🏠 Address', {
            'fields': (('current_address', 'permanent_address'),),
        }),
        ('🌏 Nationality & ID', {
            'fields': (('nationality', 'identification'),),
        }),
        ('🚨 Emergency Contact', {
            'fields': (('emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone'),),
        }),
        ('👪 Parent/Guardian', {
            'fields': (('parent_guardian',),),
        }),
        ('🎓 Academic Info', {
            'fields': (('admission_date', 'academic_year', 'degree_type', 'roll_number'),),
        }),
    )
    readonly_fields = ('roll_number', 'admission_date')
    list_display = ('roll_number', 'first_name', 'last_name', 'academic_year', 'degree_type', 'admission_date')
    search_fields = ('first_name', 'last_name', 'roll_number')
    list_filter = ('academic_year', 'degree_type', 'gender', 'current_address__country')
