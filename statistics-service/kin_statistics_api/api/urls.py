from django.urls import path

from api.views import HealthCheckView


urlpatterns = [
    path('healthcheck', HealthCheckView.as_view()),
]
