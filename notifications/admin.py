from django.contrib import admin
from django.utils.html import format_html
from .models import NotificationTemplate, NotificationSchedule, NotificationDelivery, NotificationPreference


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'channels_display', 'created_at')
    search_fields = ('name', 'subject')
    
    def channels_display(self, obj):
        return ', '.join(obj.channels)
    channels_display.short_description = 'Channels'


@admin.register(NotificationSchedule)
class NotificationScheduleAdmin(admin.ModelAdmin):
    list_display = ('template', 'scheduled_for', 'sent', 'recipient_count', 'progress')
    list_filter = ('sent', 'scheduled_for')
    readonly_fields = ('sent',)
    
    def recipient_count(self, obj):
        return obj.recipients.count()
    recipient_count.short_description = 'Recipients'
    
    def progress(self, obj):
        total = obj.deliveries.count()
        sent = obj.deliveries.filter(status='sent').count()
        if total == 0:
            return '—'
        return format_html('<b>{}/{}</b>', sent, total)
    progress.short_description = 'Sent'


@admin.register(NotificationDelivery)
class NotificationDeliveryAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'channel', 'status', 'sent_at')
    list_filter = ('status', 'channel')
    search_fields = ('recipient__username', 'recipient__email')
    readonly_fields = ('schedule', 'recipient', 'message', 'sent_at', 'error')


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_enabled', 'in_app_enabled')
    list_filter = ('email_enabled',)
