from django.utils.translation import gettext_lazy as _
from grappelli.dashboard import modules, Dashboard


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        super().init_with_context(context)

        self.children.append(modules.AppList(
            _('User Management'),
            column=1,
            models=('django.contrib.auth.*',),
            collapsible=True,
            css_classes=('collapse closed',),
        ))

        self.children.append(modules.AppList(
            _('SIS'),
            column=1,
            models=('students.*',),
            collapsible=True,
            css_classes=('collapse closed',),
        ))

        self.children.append(modules.AppList(
            _('Administration'),
            column=1,
            models=('django.contrib.*',),
            exclude=('django.contrib.auth.*',),
            collapsible=True,
            css_classes=('collapse closed',),
        ))

        self.children.append(modules.LinkList(
            _('Media Management'),
            column=2,
            children=[
                {
                    'title': _('FileBrowser'),
                    'url': '/admin/filebrowser/browse/',
                    'external': False,
                },
            ]
        ))

        self.children.append(modules.LinkList(
            _('Support'),
            column=2,
            children=[
                {
                    'title': _('Django Documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Grappelli Documentation'),
                    'url': 'http://django-grappelli.readthedocs.io/',
                    'external': True,
                },
            ]
        ))


        self.children.append(modules.Feed(
            _('Latest Django News'),
            column=2,
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5
        ))

        self.children.append(modules.RecentActions(
            _('Recent actions'),
            limit=5,
            collapsible=False,
            column=2,  # Try 1 or 2
        ))
