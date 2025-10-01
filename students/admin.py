from django.contrib import admin
from django import forms
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.admin.widgets import AdminFileWidget
from .models import Student

try:
    from intl_tel_input.widgets import IntlTelInputWidget
except Exception:
    IntlTelInputWidget = None

class StudentAdminForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        # default compact widget attrs (standard small width)
        small_style = 'width:220px;'  # standard compact width
        widgets = {
            'first_name': forms.TextInput(attrs={'style': small_style}),
            'middle_name': forms.TextInput(attrs={'style': small_style}),
            'last_name': forms.TextInput(attrs={'style': small_style}),
            'email': forms.EmailInput(attrs={'style': small_style}),
            'identification': forms.TextInput(attrs={'style': small_style}),

            'father_first_name': forms.TextInput(attrs={'style': small_style}),
            'father_middle_name': forms.TextInput(attrs={'style': small_style}),
            'father_last_name': forms.TextInput(attrs={'style': small_style}),
            'father_email': forms.EmailInput(attrs={'style': small_style}),
            'father_occupation': forms.TextInput(attrs={'style': small_style}),

            'mother_first_name': forms.TextInput(attrs={'style': small_style}),
            'mother_middle_name': forms.TextInput(attrs={'style': small_style}),
            'mother_last_name': forms.TextInput(attrs={'style': small_style}),
            'mother_email': forms.EmailInput(attrs={'style': small_style}),
            'mother_occupation': forms.TextInput(attrs={'style': small_style}),

            'current_area': forms.TextInput(attrs={'style': small_style}),
            'current_street': forms.TextInput(attrs={'style': small_style}),
            'current_pin_code': forms.TextInput(attrs={'style': small_style}),

            'permanent_area': forms.TextInput(attrs={'style': small_style}),
            'permanent_street': forms.TextInput(attrs={'style': small_style}),
            'permanent_pin_code': forms.TextInput(attrs={'style': small_style}),

            # select fields (countries/regions/cities) — keep standard small width
            'current_country': forms.Select(attrs={'style': small_style}),
            'current_region': forms.Select(attrs={'style': small_style}),
            'current_city': forms.Select(attrs={'style': small_style}),
            'permanent_country': forms.Select(attrs={'style': small_style}),
            'permanent_region': forms.Select(attrs={'style': small_style}),
            'permanent_city': forms.Select(attrs={'style': small_style}),
        }

        # wire intl-tel-input to phone fields if available (keeps country selector + number in one control)
        if IntlTelInputWidget:
            widgets.update({
                'phone': IntlTelInputWidget(attrs={'class': 'vTextField', 'style': small_style}),
                'father_phone': IntlTelInputWidget(attrs={'class': 'vTextField', 'style': small_style}),
                'mother_phone': IntlTelInputWidget(attrs={'class': 'vTextField', 'style': small_style}),
            })
        else:
            # fallback to plain input with compact style
            widgets.update({
                'phone': forms.TextInput(attrs={'style': small_style}),
                'father_phone': forms.TextInput(attrs={'style': small_style}),
                'mother_phone': forms.TextInput(attrs={'style': small_style}),
            })

        # use a compact file input for photograph to match Grappelli look
        widgets.update({
            'photograph': forms.ClearableFileInput(attrs={'style': 'width:180px;'}),
        })


class StudentAdmin(SimpleHistoryAdmin):
    form = StudentAdminForm
    fieldsets = (
        ('👤 Student Info', {
            'fields': (('first_name', 'middle_name', 'last_name'), ('date_of_birth', 'gender', 'photograph')),
        }),
        ('📞 Contact', {
            'fields': (('phone', 'email'),),
        }),
        ('🌏 ID', {
            'fields': (('identification',),),
        }),
        ('👪 Parents', {
            'fields': (
                ('father_first_name', 'father_middle_name', 'father_last_name'),
                ('father_phone', 'father_email', 'father_occupation'),
                ('mother_first_name', 'mother_middle_name', 'mother_last_name'),
                ('mother_phone', 'mother_email', 'mother_occupation'),
            ),
        }),
        ('🏠 Current Address', {
            'fields': (('current_country', 'current_region', 'current_city'), ('current_area', 'current_street', 'current_pin_code')),
        }),
        ('🏠 Permanent Address', {
            'fields': (('permanent_same_as_current', 'permanent_country', 'permanent_region', 'permanent_city'), ('permanent_area', 'permanent_street', 'permanent_pin_code')),
        }),
        ('🎓 Academic Info', {
            'fields': (('admission_date', 'academic_year', 'degree_type', 'roll_number'),),
        }),
    )
    readonly_fields = ('roll_number', 'admission_date')
    list_display = (
        'roll_number', 'first_name', 'middle_name', 'last_name', 'academic_year',
        'degree_type', 'admission_date', 'current_city', 'father_first_name', 'mother_first_name'
    )
    search_fields = ('first_name', 'last_name', 'roll_number', 'email')
    list_filter = (
        'academic_year', 'degree_type', 'gender',
        'current_country', 'current_region',
    )

admin.site.register(Student, StudentAdmin)

    # attach Media dynamically if intl widget is present
if IntlTelInputWidget:
    # we add the JS/CSS via the form admin class Media attribute
    StudentAdmin.Media = type('Media', (), {
        'js': ('intl_tel_input/js/intlTelInput.min.js',),
        'css': {'all': ('intl_tel_input/css/intlTelInput.css',)}
    })
