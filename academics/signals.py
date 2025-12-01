from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Enrollment, Course


@receiver(post_save, sender=Enrollment)
def send_welcome_notification(sender, instance, created, **kwargs):
    """Send welcome notification when student enrolls"""
    if created:
        try:
            from notifications.models import NotificationSchedule, NotificationTemplate
            from django.contrib.contenttypes.models import ContentType
                       
            template, _ = NotificationTemplate.objects.get_or_create(
                name='student_welcome',
                defaults={
                    'subject': 'Welcome to {course}!',
                    'body': 'Hi {student},\n\nWelcome to {course}! We are excited to have you join our college. Your classes will begin soon.\n\nBest regards,\nEduFlow LMS',
                    'channels': ['email']
                }
            )
            
            # Create notification schedule (send immediately)
            ct = ContentType.objects.get_for_model(Enrollment)
            schedule = NotificationSchedule.objects.create(
                content_type=ct,
                object_id=instance.pk,
                template=template,
                scheduled_for=timezone.now(),  # Send now
                context={
                    'student': instance.student.get_full_name() or instance.student.username,
                    'course': instance.course.title,
                },
                sent=False,
            )
            schedule.recipients.add(instance.student)
            
        except ImportError:
            pass


@receiver(post_save, sender=Course)
def notify_teacher_assignment(sender, instance, created, **kwargs):
    """Notify teacher when assigned to course"""
    if not created and instance.teacher:
        try:
            from notifications.models import NotificationSchedule, NotificationTemplate
            from django.contrib.contenttypes.models import ContentType
            
            template, _ = NotificationTemplate.objects.get_or_create(
                name='teacher_assignment',
                defaults={
                    'subject': 'You have been assigned to {course}',
                    'body': 'Hi {teacher},\n\nYou have been assigned as the teacher for {course}. Students enrolled: {student_count}.\n\nBest regards,\nEduFlow LMS',
                    'channels': ['email']
                }
            )
            
            ct = ContentType.objects.get_for_model(Course)
            schedule, created_schedule = NotificationSchedule.objects.get_or_create(
                content_type=ct,
                object_id=instance.pk,
                defaults={
                    'template': template,
                    'scheduled_for': timezone.now(),
                    'context': {
                        'teacher': instance.teacher.get_full_name() or instance.teacher.username,
                        'course': instance.title,
                        'student_count': instance.enrollments.count(),
                    },
                    'sent': False,
                }
            )
            
            if created_schedule:
                schedule.recipients.add(instance.teacher)
            
        except ImportError:
            pass