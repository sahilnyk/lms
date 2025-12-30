from django.utils.translation import gettext_lazy as _
from grappelli.dashboard import modules, Dashboard

class CustomDashboard(Dashboard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = _('Platform Control')

        self.children.append(modules.AppList(
            title=_('Organisation Management'),
            column=1,
            collapsible=True,
            models=(
                'tenancy.models.Organisation',
            ),
            css_classes=['grp-collapse', 'grp-open'],
        ))

        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            column=2,
            collapsible=True,
            limit=10,
        ))
