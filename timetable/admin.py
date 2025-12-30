from django.contrib import admin
from django.utils.html import format_html
from django import forms

from .models import TimeTable, TimetableNotification, ClassSession


class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time")

        return cleaned_data


@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    form = TimeTableForm
    list_display = (
        "course",
        "lesson",
        "teacher",
        "day_display",
        "time_display",
        "is_active",
    )
    list_filter = ("day_of_week", "is_active", "course")
    search_fields = ("course__title", "lesson__title", "teacher__username")
    list_editable = ("is_active",)

    def day_display(self, obj):
        colors = {
            "monday": "#2196F3",
            "tuesday": "#4CAF50",
            "wednesday": "#FF9800",
            "thursday": "#9C27B0",
            "friday": "#F44336",
            "saturday": "#795548",
        }
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}</span>',
            colors.get(obj.day_of_week, "#000"),
            obj.get_day_of_week_display(),
        )

    day_display.short_description = "Day"

    def time_display(self, obj):
        return f"{obj.start_time.strftime('%H:%M')} - {obj.end_time.strftime('%H:%M')}"

    time_display.short_description = "Time"


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = (
        "course",
        "lesson_display",
        "start_at",
        "duration_minutes",
        "active",
        "notification_status",
    )
    list_filter = ("active", "course", "start_at")
    search_fields = ("course__title", "lesson__title", "title")
    list_editable = ("active",)
    date_hierarchy = "start_at"

    def lesson_display(self, obj):
        return obj.lesson.title if obj.lesson else obj.title or "—"

    lesson_display.short_description = "Lesson"

    def notification_status(self, obj):
        try:
            from notifications.models import NotificationSchedule
            from django.contrib.contenttypes.models import ContentType

            ct = ContentType.objects.get_for_model(ClassSession)
            schedule = NotificationSchedule.objects.filter(
                content_type=ct, object_id=obj.pk
            ).first()

            if schedule:
                if schedule.sent:
                    return format_html('<span style="color:#4CAF50;">✓ Sent</span>')
                return format_html('<span style="color:#FF9800;">⏱ Scheduled</span>')
            return "—"
        except Exception:
            return "—"

    notification_status.short_description = "Notification"


@admin.register(TimetableNotification)
class TimetableNotificationAdmin(admin.ModelAdmin):
    list_display = (
        "timetable_entry",
        "notification_type",
        "is_sent",
        "sent_at",
    )
    list_filter = ("notification_type", "is_sent")
    readonly_fields = ("sent_at",)
