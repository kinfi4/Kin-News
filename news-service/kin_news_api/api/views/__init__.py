from django.conf import settings

from .user import UserView, LoginView, RegisterView
from .channels import ChannelListView

from config.containers import Container
from api import views

container = Container()
container.config.from_dict(settings.__dict__)
container.init_resources()
container.wire(packages=[views])
