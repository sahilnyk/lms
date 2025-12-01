from django.core.management.base import BaseCommand
from notifications.tasks import enqueue_due_notifications


class Command(BaseCommand):
    help = 'Enqueue due notifications'
    
    def handle(self, *args, **options):
        result = enqueue_due_notifications()
        self.stdout.write(self.style.SUCCESS(result))