import uuid
from django.db import models

class Organisation(models.Model):
    STATUS_CHOICES = (
        ("ACTIVE", "ACTIVE"),
        ("SUSPENDED", "SUSPENDED"),
    )
    
    SIZE_CHOICES = (
        ('1-50', '1-50 users'),
        ('51-200', '51-200 users'),
        ('201-500', '201-500 users'),
        ('500+', '500+ users'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, db_index=True)

    owner_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    address = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, blank=True, null=True)

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="ACTIVE")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Add subscription_status as a property for admin display/filter
    @property
    def subscription_status(self):
        # Example logic: you can replace this with your actual subscription logic
        if self.status == "ACTIVE":
            return "Active"
        elif self.status == "SUSPENDED":
            return "Suspended"
        return "Unknown"

    def __str__(self):
        return f"{self.name} ({self.slug})"
