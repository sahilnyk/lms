import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Schedule to check for notifications every minute
app.conf.beat_schedule = {
    'enqueue-notifications-every-minute': {
        'task': 'notifications.tasks.enqueue_due_notifications',
        'schedule': crontab(minute='*'),
    },
}