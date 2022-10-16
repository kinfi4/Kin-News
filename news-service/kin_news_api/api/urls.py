from django.urls import path

from api.views import RegisterView, LoginView, UserView, ChannelListView


urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('me', UserView.as_view()),
    path('channels', ChannelListView.as_view()),
]
