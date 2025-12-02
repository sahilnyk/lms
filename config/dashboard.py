from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from grappelli.dashboard import modules, Dashboard


class CustomDashboard(Dashboard):
    """
    Custom dashboard for EduFlow LMS
    """
    
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)
        self.title = _('EduFlow Dashboard')
        
        # Column 1 - Academic Management
        self.children.append(modules.AppList(
            title=_('Academic Management'),
            column=1,
            collapsible=True,
            models=(
                'academics.models.Course',
                'academics.models.Lesson',
                'academics.models.LessonChecklistItem',
            ),
            css_classes=['grp-collapse', 'grp-open'],
        ))
        
        self.children.append(modules.AppList(
            title=_('Enrollment & Progress'),
            column=1,
            collapsible=True,
            models=(
                'academics.models.Enrollment',
                'academics.models.LessonProgress',
            ),
            css_classes=['grp-collapse', 'grp-open'],
        ))
        
        self.children.append(modules.AppList(
            title=_('Timetable Management'),
            column=1,
            collapsible=True,
            models=(
                'timetable.models.TimeTable',
                'timetable.models.ClassSession',
                'timetable.models.TimetableNotification',
            ),
            css_classes=['grp-collapse', 'grp-open'],
        ))
        
        # Column 2 - Users & Notifications
        self.children.append(modules.AppList(
            title=_('User Management'),
            column=2,
            collapsible=True,
            models=(
                'django.contrib.auth.models.User',
                'django.contrib.auth.models.Group',
            ),
            css_classes=['grp-collapse', 'grp-open'],
        ))
        
        self.children.append(modules.AppList(
            title=_('Notification System'),
            column=2,
            collapsible=True,
            models=(
                'notifications.models.NotificationTemplate',
                'notifications.models.NotificationSchedule',
                'notifications.models.NotificationDelivery',
                'notifications.models.NotificationPreference',
            ),
            css_classes=['grp-collapse', 'grp-open'],
        ))
        
        self.children.append(modules.AppList(
            title=_('Task Scheduling'),
            column=2,
            collapsible=True,
            models=(
                'django_celery_beat.*',
            ),
            css_classes=['grp-collapse', 'grp-open'],
        ))
        
        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            column=2,
            collapsible=True,
            limit=10,
        ))
        
        # Column 3 - Links
        self.children.append(modules.LinkList(
            title=_('Quick Links'),
            column=1,
            collapsible=True,
            children=[
                {
                    'title': _('Add New Course'),
                    'url': '/admin/academics/course/add/',
                    'external': False,
                },
                {
                    'title': _('Add New Lesson'),
                    'url': '/admin/academics/lesson/add/',
                    'external': False,
                },
                {
                    'title': _('Add Class Session'),
                    'url': '/admin/timetable/classsession/add/',
                    'external': False,
                },
                {
                    'title': _('View Enrollments'),
                    'url': '/admin/academics/enrollmentadminproxy/',
                    'external': False,
                },
                {
                    'title': _('Notification Templates'),
                    'url': '/admin/notifications/notificationtemplate/',
                    'external': False,
                },
            ],
            css_classes=['grp-collapse', 'grp-open'],
        ))
        
        self.children.append(modules.LinkList(
            title=_('System & Documentation'),
            column=3,
            collapsible=True,
            children=[
                {
                    'title': _('Django Documentation'),
                    'url': 'https://docs.djangoproject.com/',
                    'external': True,
                    'target': '_blank',
                },
                {
                    'title': _('Grappelli Documentation'),
                    'url': 'https://django-grappelli.readthedocs.io/',
                    'external': True,
                    'target': '_blank',
                },
                {
                    'title': _('Celery Documentation'),
                    'url': 'https://docs.celeryproject.org/',
                    'external': True,
                    'target': '_blank',
                },
                {
                    'title': _('CKEditor Documentation'),
                    'url': 'https://ckeditor.com/docs/',
                    'external': True,
                    'target': '_blank',
                },
            ],
            css_classes=['grp-collapse', 'grp-closed'],
        ))