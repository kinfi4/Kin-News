from .healthcheck import HealthCheckView
from .reports import ReportsSingleView, ReportsListView
from .register_user import RegisterUserView

from config.containers import Container
from config import settings
from api import views

container = Container()
container.config.from_dict(settings.__dict__)
container.init_resources()
container.wire(
    packages=[views]
)
