from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import ClassSession, TimeTable


@receiver(post_save, sender=TimeTable)
def notify_timetable_change(sender, instance, created, **kwargs):
    """Notify students when timetable is added or changed"""
    try:
        from notifications.models import NotificationSchedule, NotificationTemplate
        from django.contrib.contenttypes.models import ContentType
        
        if created:
            template_name = 'timetable_added'
            subject = 'New Class Added: {course}'
            body = 'Hi {student},\n\nA new class has been added to your timetable:\n\nCourse: {course}\nDay: {day}\nTime: {time}\nLocation: {location}\n\nBest regards,\nEduFlow LMS'
        else:
            template_name = 'timetable_updated'
            subject = 'Timetable Updated: {course}'
            body = 'Hi {student},\n\nYour timetable has been updated:\n\nCourse: {course}\nDay: {day}\nTime: {time}\nLocation: {location}\n\nBest regards,\nEduFlow LMS'
        
        template, _ = NotificationTemplate.objects.get_or_create(
            name=template_name,
            defaults={
                'subject': subject,
                'body': body,
                'channels': ['email']
            }
        )
        
        # Get enrolled students
        students = instance.course.enrollments.values_list('student', flat=True)
        
        ct = ContentType.objects.get_for_model(TimeTable)
        schedule = NotificationSchedule.objects.create(
            content_type=ct,
            object_id=instance.pk,
            template=template,
            scheduled_for=timezone.now(),
            context={
                'student': 'Student',
                'course': instance.course.title,
                'day': instance.get_day_of_week_display(),
                'time': f"{instance.start_time.strftime('%H:%M')} - {instance.end_time.strftime('%H:%M')}",
                'location': instance.location or 'TBA',
            },
            sent=False,
        )
        schedule.recipients.set(students)
        
    except ImportError:
        pass


@receiver(post_delete, sender=ClassSession)
def delete_notification_schedule(sender, instance, **kwargs):
    """Delete notification when class is deleted"""
    try:
        from notifications.models import NotificationSchedule
        from django.contrib.contenttypes.models import ContentType
        
        ct = ContentType.objects.get_for_model(ClassSession)
        NotificationSchedule.objects.filter(content_type=ct, object_id=instance.pk).delete()
    except ImportError:
        pass