import uuid
from django.db import models
from django.utils.text import slugify

class Organisation(models.Model):
    STATUS_CHOICES = (
        ("ACTIVE", "ACTIVE"),
        ("SUSPENDED", "SUSPENDED"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    subscription_plan = models.CharField(max_length=50, blank=True, null=True)
    subscription_status = models.CharField(max_length=50, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
