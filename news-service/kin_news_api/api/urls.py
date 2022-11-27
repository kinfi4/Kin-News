from django.urls import path

from api.views import (
    RegisterView,
    LoginView,
    UserView,
    ChannelListView,
    ChannelRateView,
    ChannelUnsubscribeView,
    HealthCheckView,
    MessagesView,
    ChannelExistsView,
)


urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('me', UserView.as_view()),
    path('channels', ChannelListView.as_view()),
    path('channels/rates', ChannelRateView.as_view()),
    path('channels/<str:channel>', ChannelUnsubscribeView.as_view()),
    path('healthcheck', HealthCheckView.as_view()),
    path('messages', MessagesView.as_view()),
    path('channels/exists/<str:channel>', ChannelExistsView.as_view()),
]
