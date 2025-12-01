from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from academics.models import Course, Lesson
from ckeditor.fields import RichTextField


class TimeTable(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetable_entries')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='timetable_entries', null=True, blank=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='timetable_entries')
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=255, blank=True, help_text="Room number or location")
    notes = RichTextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['day_of_week', 'start_time']
        verbose_name = 'Time Table Entry'
        verbose_name_plural = 'Time Table Entries'
    
    def __str__(self):
        return f"{self.course.title} - {self.get_day_of_week_display()} {self.start_time.strftime('%H:%M')}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.start_time >= self.end_time:
            raise ValidationError('End time must be after start time')


class TimetableNotification(models.Model):
    NOTIFICATION_TYPE = [
        ('upcoming_class', 'Upcoming Class'),
        ('class_cancelled', 'Class Cancelled'),
        ('class_rescheduled', 'Class Rescheduled'),
        ('reminder', 'Reminder'),
    ]
    
    timetable_entry = models.ForeignKey(TimeTable, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE)
    message = RichTextField()
    send_to_students = models.BooleanField(default=True)
    send_to_teachers = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Timetable Notification'
        verbose_name_plural = 'Timetable Notifications'
    
    def __str__(self):
        return f"{self.notification_type} - {self.timetable_entry}"


# ADD THIS NEW MODEL
class ClassSession(models.Model):
    """Scheduled class with automatic notifications"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='class_sessions')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='class_sessions', null=True, blank=True)
    title = models.CharField(max_length=200, blank=True)
    description = RichTextField(blank=True)
    start_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    notify_before_minutes = models.PositiveIntegerField(default=10)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_at']
        verbose_name = 'Class Session'
        verbose_name_plural = 'Class Sessions'
    
    def __str__(self):
        lesson_title = self.lesson.title if self.lesson else self.title or "Session"
        return f"{self.course.title} - {lesson_title} @ {self.start_at.strftime('%Y-%m-%d %H:%M')}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        try:
            from notifications.models import NotificationSchedule, NotificationTemplate
            from django.contrib.contenttypes.models import ContentType
            
            scheduled_for = self.start_at - timedelta(minutes=self.notify_before_minutes)
            
            template, _ = NotificationTemplate.objects.get_or_create(
                name='upcoming_class',
                defaults={
                    'subject': 'Upcoming Class: {course}',
                    'body': 'Your class "{lesson}" for {course} starts at {start_at}. Duration: {duration} minutes.',
                    'channels': ['email']
                }
            )
            
            recipients = self.course.enrollments.values_list('student', flat=True)
            
            context = {
                'course': self.course.title,
                'lesson': self.lesson.title if self.lesson else self.title or 'General Session',
                'start_at': self.start_at.strftime('%Y-%m-%d %H:%M'),
                'duration': self.duration_minutes,
            }
            
            if self.active:
                ct = ContentType.objects.get_for_model(self)
                schedule, created = NotificationSchedule.objects.update_or_create(
                    content_type=ct,
                    object_id=self.pk,
                    defaults={
                        'template': template,
                        'scheduled_for': scheduled_for,
                        'context': context,
                        'sent': False,
                    }
                )
                schedule.recipients.set(recipients)
            else:
                ct = ContentType.objects.get_for_model(self)
                NotificationSchedule.objects.filter(content_type=ct, object_id=self.pk).delete()
        
        except ImportError:
            pass
