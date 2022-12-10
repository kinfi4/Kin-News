from django.urls import path

from api.views import (
    HealthCheckView,
    ReportsSingleView,
    ReportsListView,
    RegisterUserView,
    GetReportDataView,
)


urlpatterns = [
    path('healthcheck', HealthCheckView.as_view()),
    path('reports', ReportsListView.as_view()),
    path('reports/<int:report_id>', ReportsSingleView.as_view()),
    path('users', RegisterUserView.as_view()),
    path('data/<int:report_id>', GetReportDataView.as_view())
]
