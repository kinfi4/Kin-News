from .healthcheck import HealthCheckView
from .reports import ReportsSingleView, ReportsListView
from .register_user import RegisterUserView
from .report_data import GetReportDataView

from config.containers import Container
from config import settings
from api import views, tasks

container = Container()
container.config.from_dict(settings.__dict__)
container.init_resources()
container.wire(
    packages=[views],
    modules=[tasks],
)
