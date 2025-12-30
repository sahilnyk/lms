from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from datetime import timedelta

from .models import ClassSession, TimeTable


@receiver(post_save, sender=TimeTable)
def notify_timetable_change(sender, instance, created, **kwargs):
    try:
        from django.contrib.contenttypes.models import ContentType
        from notifications.models import NotificationSchedule, NotificationTemplate
        from django.utils import timezone

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
            defaults={'subject': subject, 'body': body, 'channels': ['email']}
        )

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
                'day': getattr(instance, 'get_day_of_week_display', lambda: '')(),
                'time': f"{getattr(instance, 'start_time', '')} - {getattr(instance, 'end_time', '')}",
                'location': getattr(instance, 'location', 'TBA'),
            },
            sent=False,
        )
        schedule.recipients.set(students)
    except Exception:
        pass


@receiver(post_save, sender=ClassSession)
def classsession_post_save(sender, instance, created, **kwargs):
    try:
        instance.schedule_notifications()
    except Exception:
        pass

    try:
        from schedule.models import Calendar, Event
        from .models import EventLink

        cal, _ = Calendar.objects.get_or_create(name="Class Sessions")
        end_time = instance.start_at + timedelta(minutes=instance.duration_minutes)
        title = f"{instance.course.title} - {instance.title or ''}".strip()

        link = getattr(instance, "event_link", None)
        if link and getattr(link, "event_id", None):
            try:
                ev = Event.objects.get(id=link.event_id)
                ev.title = title
                ev.start = instance.start_at
                ev.end = end_time
                ev.save()
            except Event.DoesNotExist:
                ev = Event.objects.create(calendar=cal, title=title, start=instance.start_at, end=end_time)
                EventLink.objects.update_or_create(class_session=instance, defaults={'event_id': ev.id, 'course': instance.course, 'lesson': instance.lesson})
        else:
            ev = Event.objects.create(calendar=cal, title=title, start=instance.start_at, end=end_time)
            try:
                EventLink.objects.update_or_create(class_session=instance, defaults={'event_id': ev.id, 'course': instance.course, 'lesson': instance.lesson})
            except Exception:
                pass
    except Exception:
        pass


@receiver(post_delete, sender=ClassSession)
def classsession_post_delete(sender, instance, **kwargs):
    try:
        from schedule.models import Event
        link = getattr(instance, "event_link", None)
        if link and getattr(link, "event_id", None):
            Event.objects.filter(id=link.event_id).delete()
            try:
                link.delete()
            except Exception:
                pass
    except Exception:
        pass

    try:
        from django.contrib.contenttypes.models import ContentType
        from notifications.models import NotificationSchedule

        ct = ContentType.objects.get_for_model(ClassSession)
        NotificationSchedule.objects.filter(content_type=ct, object_id=instance.pk).delete()
    except Exception:
        pass