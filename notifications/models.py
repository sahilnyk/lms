from django.db import models
from django.conf import settings
from django.utils import timezone
from ckeditor.fields import RichTextField


class NotificationTemplate(models.Model):
    """Templates for notifications"""
    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=200)
    body = RichTextField(help_text="Use {course}, {lesson}, {start_at}, {duration}")
    channels = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class NotificationSchedule(models.Model):
    """Scheduled notification for a class session"""
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    template = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE, related_name='schedules')
    scheduled_for = models.DateTimeField(db_index=True)
    context = models.JSONField(default=dict)
    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='notification_schedules')
    channels = models.JSONField(default=list)
    sent = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['scheduled_for']
        indexes = [
            models.Index(fields=['scheduled_for', 'sent']),
        ]
    
    def __str__(self):
        return f"{self.template.name} @ {self.scheduled_for}"


class NotificationDelivery(models.Model):
    """Individual delivery per user"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]
    CHANNEL_CHOICES = [
        ('email', 'Email'),
        ('in_app', 'In-App'),
        ('push', 'Push'),
    ]
    
    schedule = models.ForeignKey(NotificationSchedule, on_delete=models.CASCADE, related_name='deliveries')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_deliveries')
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', db_index=True)
    message = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True)
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = [('schedule', 'recipient', 'channel')]
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.recipient.username} - {self.channel} - {self.status}"


class NotificationPreference(models.Model):
    """User notification preferences"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_preferences')
    email_enabled = models.BooleanField(default=True)
    in_app_enabled = models.BooleanField(default=True)
    push_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} preferences"
