from dependency_injector.wiring import inject, Provide

from api.domain.services import IGeneratingReportsService
from api.domain.entities import GenerateReportEntity
from config.celery import celery_app
from config.containers import Container


@celery_app.task
@inject
def generate_report_task(
    start_date: str,
    end_date: str,
    channel_list: list[str],
    user_id: int,
    generating_reports_service: IGeneratingReportsService = Provide[Container.services.generating_reports_service],
) -> None:
    generate_report_entity = GenerateReportEntity(
        start_date=start_date,
        end_date=end_date,
        channel_list=channel_list,
    )

    generating_reports_service.generate_report(generate_report_entity, user_id)
