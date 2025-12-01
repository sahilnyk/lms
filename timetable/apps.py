from django.apps import AppConfig


class TimetableConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'timetable'
    verbose_name = 'Time Table'

    def ready(self):
        import timetable.signals