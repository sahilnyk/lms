from django.db import models
from simple_history.models import HistoricalRecords

DEGREE_TYPE_CHOICES = [
    ('UG', 'Undergraduate'),
    ('PG', 'Postgraduate'),
]

class Student(models.Model):
    # Basic Info
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    # Address (broken down)
    street_name = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    
    # Parent Details
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    parent_contact_number = models.CharField(max_length=15)
    parent_email = models.EmailField()
    
    # Admission & Academic Info
    admission_date = models.DateField(auto_now_add=True)
    academic_year = models.CharField(max_length=9)  # e.g., "2024-2025"
    degree_type = models.CharField(max_length=2, choices=DEGREE_TYPE_CHOICES)
    roll_number = models.CharField(max_length=30, unique=True, editable=False)
    
    # History tracking
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        # Auto-generate roll number if not set
        if not self.roll_number:
            # Example: UG-2024-0001
            year = self.academic_year.split('-')[0] if self.academic_year else 'YYYY'
            code = self.degree_type
            last_id = Student.objects.filter(
                academic_year=self.academic_year,
                degree_type=self.degree_type
            ).count() + 1
            self.roll_number = f"{code}-{year}-{last_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.roll_number})"

