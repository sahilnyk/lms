from django.db import models
from simple_history.models import HistoricalRecords
from phonenumber_field.modelfields import PhoneNumberField
from smart_selects.db_fields import ChainedForeignKey

# cities_light models are provided by django-cities-light
# make sure 'cities_light' is in INSTALLED_APPS and you've loaded the data
# (cities_light.models.Country, Region, City)

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

class Student(models.Model):
    # Identification / basic
    roll_number = models.CharField(max_length=30, unique=True, editable=False)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)

    # Personal
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    photograph = models.ImageField(upload_to='students/photos/', blank=True, null=True)

    # Contact (uses intl widget in admin via form)
    phone = PhoneNumberField(region=None)
    email = models.EmailField()

    # ID
    identification = models.CharField(max_length=100, help_text="Aadhaar, Passport, SSN, etc.", blank=True, null=True)

    # Parents (kept inline in same model as requested)
    father_first_name = models.CharField(max_length=50, blank=True, null=True)
    father_middle_name = models.CharField(max_length=50, blank=True, null=True)
    father_last_name = models.CharField(max_length=50, blank=True, null=True)
    father_phone = PhoneNumberField(region=None, blank=True, null=True)
    father_email = models.EmailField(blank=True, null=True)
    father_occupation = models.CharField(max_length=100, blank=True, null=True)

    mother_first_name = models.CharField(max_length=50, blank=True, null=True)
    mother_middle_name = models.CharField(max_length=50, blank=True, null=True)
    mother_last_name = models.CharField(max_length=50, blank=True, null=True)
    mother_phone = PhoneNumberField(region=None, blank=True, null=True)
    mother_email = models.EmailField(blank=True, null=True)
    mother_occupation = models.CharField(max_length=100, blank=True, null=True)

    # Address - uses django-cities-light with smart-selects for chained dropdowns
    # current address
    current_country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    current_region = ChainedForeignKey(
        'cities_light.Region',
        chained_field='current_country',
        chained_model_field='country',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    current_city = ChainedForeignKey(
        'cities_light.City',
        chained_field='current_region',
        chained_model_field='region',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    current_area = models.CharField(max_length=100, null=True, blank=True)
    current_street = models.CharField(max_length=100, null=True, blank=True)
    current_pin_code = models.CharField(max_length=20, null=True, blank=True)

    # permanent address
    permanent_same_as_current = models.BooleanField(default=False)
    permanent_country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    permanent_region = ChainedForeignKey(
        'cities_light.Region',
        chained_field='permanent_country',
        chained_model_field='country',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    permanent_city = ChainedForeignKey(
        'cities_light.City',
        chained_field='permanent_region',
        chained_model_field='region',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+'
    )
    permanent_area = models.CharField(max_length=100, null=True, blank=True)
    permanent_street = models.CharField(max_length=100, null=True, blank=True)
    permanent_pin_code = models.CharField(max_length=20, null=True, blank=True)

    # Other academic
    admission_date = models.DateField(auto_now_add=True)
    academic_year = models.CharField(max_length=9, null=True, blank=True)  # e.g., "2024-2025"
    degree_type = models.CharField(
        max_length=2,
        choices=[('UG', 'Undergraduate'), ('PG', 'Postgraduate')],
        null=True,
        blank=True
    )

    # history
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        # copy current -> permanent if requested
        if self.permanent_same_as_current:
            self.permanent_country = self.current_country
            self.permanent_region = self.current_region
            self.permanent_city = self.current_city
            self.permanent_area = self.current_area
            self.permanent_street = self.current_street
            self.permanent_pin_code = self.current_pin_code

        # Auto-generate roll number if not set
        if not self.roll_number:
            year = self.academic_year.split('-')[0] if self.academic_year else 'YYYY'
            code = self.degree_type if self.degree_type else 'XX'
            last_id = Student.objects.filter(
                academic_year=self.academic_year,
                degree_type=self.degree_type
            ).count() + 1
            self.roll_number = f"{code}-{year}-{last_id:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.roll_number})"

