from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail, get_connection
from django.template.loader import render_to_string
from django.conf import settings
from .models import NotificationSchedule, NotificationDelivery, NotificationPreference
import logging

logger = logging.getLogger(__name__)


@shared_task
def enqueue_due_notifications():
    """Find and enqueue due notifications"""
    now = timezone.now()
    
    due_schedules = NotificationSchedule.objects.filter(
        scheduled_for__lte=now,
        sent=False
    ).prefetch_related('recipients')
    
    count = 0
    for schedule in due_schedules:
        channels = schedule.channels or schedule.template.channels
        recipients = schedule.recipients.all()
        
        message = schedule.template.body.format(**schedule.context)
        subject = schedule.template.subject.format(**schedule.context)
        
        for recipient in recipients:
            try:
                prefs = recipient.notification_preferences
            except NotificationPreference.DoesNotExist:
                prefs = NotificationPreference.objects.create(user=recipient)
            
            for channel in channels:
                if channel == 'email' and not prefs.email_enabled:
                    continue
                
                delivery, created = NotificationDelivery.objects.get_or_create(
                    schedule=schedule,
                    recipient=recipient,
                    channel=channel,
                    defaults={'message': message, 'status': 'pending'}
                )
                
                if created:
                    send_notification.delay(delivery.id, subject, message)
                    count += 1
        
        schedule.sent = True
        schedule.save(update_fields=['sent'])
    
    logger.info(f"Enqueued {count} notifications")
    return f"Processed {due_schedules.count()} schedules"


@shared_task(bind=True, max_retries=3)
def send_notification(self, delivery_id, subject, message):
    """Send notification via email"""
    try:
        delivery = NotificationDelivery.objects.select_related('recipient').get(id=delivery_id)
        
        if delivery.status == 'sent':
            return f"Already sent"
        
        if delivery.channel == 'email':
            # Create new connection for each email
            connection = get_connection(
                backend='django.core.mail.backends.smtp.EmailBackend',
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS,
                fail_silently=False,
            )
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [delivery.recipient.email],
                fail_silently=False,
                connection=connection,
            )
            
            connection.close()
        
        delivery.status = 'sent'
        delivery.sent_at = timezone.now()
        delivery.save(update_fields=['status', 'sent_at'])
        
        logger.info(f"Sent to {delivery.recipient.email}")
        return f"Sent successfully"
    
    except Exception as exc:
        logger.error(f"Failed: {str(exc)}")
        delivery.status = 'failed'
        delivery.error = str(exc)
        delivery.save(update_fields=['status', 'error'])
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True, ignore_result=True)
def send_notification_task(self, subject: str, title: str, message: str,
                           recipients: list, course: dict = None,
                           action_url: str | None = None, action_text: str | None = "View"):
    if not recipients:
        return {"error": "no recipients"}

    timestamp = timezone.now().isoformat()
    context = {
        "subject": subject,
        "title": title,
        "message": message,
        "timestamp": timestamp,
        "course": course or {},
        "action_url": action_url,
        "action_text": action_text,
        "recipient": ", ".join(recipients),
    }

    try:
        html = render_to_string("notifications/email/notification.html", context)
    except Exception:
        html = None

    try:
        text = render_to_string("notifications/email/notification.txt", context)
    except Exception:
        text = f"{title}\n\n{message}\n\nCourse: {course.get('title') if course else ''}\n\n{action_url or ''}"

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(settings, "EMAIL_FROM", None) or None

    try:
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
            fail_silently=False,
        )
        
        send_mail(
            subject,
            text,
            from_email,
            recipients,
            html_message=html,
            fail_silently=False,
            connection=connection,
        )
        
        connection.close()
    except Exception as exc:
        logger.error(f"send_notification_task failed: {str(exc)}")
        return {"error": "send_failed", "detail": str(exc)}

    for r in recipients:
        try:
            NotificationDelivery.objects.create(
                recipient_id=None,
                subject=subject,
                body=message,
                message=message,
                channel='email',
                status='sent',
                sent_at=timezone.now(),
            )
        except Exception:
            continue

    return {"status": "sent", "recipients_count": len(recipients)}