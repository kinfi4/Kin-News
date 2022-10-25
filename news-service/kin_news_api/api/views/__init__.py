from .user import UserView, LoginView, RegisterView
from .channels import ChannelListView, ChannelUnsubscribeView
from .ratings import ChannelRateView
from .healthcheck import HealthCheckView

from config.containers import Container
from config import settings
from api import views

container = Container()
container.config.from_dict(settings.__dict__)
container.init_resources()
container.wire(packages=[views])
