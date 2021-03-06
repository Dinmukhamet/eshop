from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard, AppIndexDashboard
#from jet.dashboard.dashboard_modules import google_analytics


class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.available_children.append(modules.LinkList)
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('auth.*',),
            column=0,
            order=0
        ))

        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            10,
            column=0,
            order=0
        ))

 #       self.available_children.append(google_analytics.GoogleAnalyticsVisitorsTotals)
 #       self.available_children.append(google_analytics.GoogleAnalyticsVisitorsChart)
 #       self.available_children.append(google_analytics.GoogleAnalyticsPeriodVisitors)
