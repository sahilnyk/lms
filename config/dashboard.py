from django.utils.translation import gettext_lazy as _
from grappelli.dashboard import modules, Dashboard


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """
    def init_with_context(self, context):
        super().init_with_context(context)

        # == COLUMN 1 (Wider: 8/12 width) ==
        # We wrap all column 1 modules in a single Group
        self.children.append(modules.Group(
            title="Main Content",
            column=1,
            # This class makes the column take up 8/12 of the width
            classes=('grp-collapse grp-open grp-grid-8',),
            children=[
                modules.Group(
                    _('Management'),
                    collapsible=True,
                    children=[
                        modules.AppList(
                            _('User Management'),
                            models=('django.contrib.auth.*',),
                        ),
                        modules.AppList(
                            _('Student Management'),
                            models=('students.*',),
                        ),
                    ]
                ),
                modules.LinkList(
                    _('Quick Links'),
                    children=[
                        {'title': _('FileBrowser'), 'url': '/admin/filebrowser/browse/', 'external': False},
                        {'title': _('Django Docs'), 'url': 'https://docs.djangoproject.com/', 'external': True},
                        {'title': _('Grappelli Docs'), 'url': 'https://django-grappelli.readthedocs.io/', 'external': True},
                    ]
                )
            ]
        ))

        # == COLUMN 2 (Narrower: 4/12 width) ==
        # We wrap all column 2 modules in another single Group
        self.children.append(modules.Group(
            title="Sidebar",
            column=2,
            # This class makes the column take up 4/12 of the width
            classes=('grp-collapse grp-open grp-grid-4',),
            children=[
                modules.ModelList(
                    _('Students'),
                    models=('students.Student',),
                ),
                modules.RecentActions(
                    _('Recent Actions'),
                    limit=5,
                ),
                modules.LinkList(
                    _('Shortcuts'),
                    children=[
                        {'title': _('Add Student'), 'url': '/admin/students/student/add/', 'external': False},
                        {'title': _('View Students'), 'url': '/admin/students/student/', 'external': False},
                        {'title': _('Manage Users'), 'url': '/admin/auth/user/', 'external': False},
                    ]
                ),
                modules.Feed(
                    _('Latest Django News'),
                    feed_url='http://www.djangoproject.com/rss/weblog/',
                    limit=5
                ),
            ]
        ))