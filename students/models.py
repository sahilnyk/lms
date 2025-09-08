from django.db import models
from simple_history.models import HistoricalRecords
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

class Address(models.Model):
    country = CountryField()
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    area = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    address_type = models.CharField(max_length=10, choices=[('current', 'Current'), ('permanent', 'Permanent')])

    def __str__(self):
        return f"{self.street_name}, {self.area}, {self.city}, {self.state}, {self.country.name} - {self.pin_code}"

class ParentGuardian(models.Model):
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone = PhoneNumberField(region=None)
    email = models.EmailField()
    address = models.TextField()
    occupation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.relationship})"

class Student(models.Model):
    roll_number = models.CharField(max_length=30, unique=True, editable=False)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    photograph = models.ImageField(upload_to='students/photos/', blank=True, null=True)
    phone = PhoneNumberField(region=None)
    email = models.EmailField()
    nationality = models.CharField(max_length=50, blank=True)
    identification = models.CharField(max_length=100, help_text="Aadhaar, Passport, SSN, etc.", blank=True)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_relationship = models.CharField(max_length=50)
    emergency_contact_phone = PhoneNumberField(region=None)
    parent_guardian = models.ForeignKey(ParentGuardian, on_delete=models.SET_NULL, null=True, blank=True)
    current_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_students')
    permanent_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='permanent_students')
    admission_date = models.DateField(auto_now_add=True)
    academic_year = models.CharField(max_length=9)  # e.g., "2024-2025"
    degree_type = models.CharField(max_length=2, choices=[('UG', 'Undergraduate'), ('PG', 'Postgraduate')])
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        # Auto-generate roll number if not set
        if not self.roll_number:
            year = self.academic_year.split('-')[0] if self.academic_year else 'YYYY'
            code = self.degree_type
            last_id = Student.objects.filter(
                academic_year=self.academic_year,
                degree_type=self.degree_type
            ).count() + 1
            self.roll_number = f"{code}-{year}-{last_id:04d}"
        # Auto-set nationality based on current address country
        if self.current_address and not self.nationality:
            self.nationality = self.current_address.country.name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.roll_number})"

