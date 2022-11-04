import logging
from datetime import datetime

from django.contrib.auth.models import User

from api.domain.services.reports_generator import IGeneratingReportsService
from api.infrastructure.repositories import IReportRepository, ReportsAccessManagementRepository
from api.domain.entities import GenerateReportEntity, ReportGetEntity
from api.domain.services.reports_generator.reports_builder import ReportsBuilder
from kin_news_core.telegram.interfaces import ITelegramProxy
from config.constants import DEFAULT_DATE_FORMAT


class GeneratingReportsService(IGeneratingReportsService):
    def __init__(
        self,
        telegram_client: ITelegramProxy,
        reports_repository: IReportRepository,
        report_access_repository: ReportsAccessManagementRepository,
    ) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)
        self._telegram = telegram_client
        self._reports_repository = reports_repository
        self._access_repository = report_access_repository

    def generate_report(self, generate_report_entity: GenerateReportEntity, user: User) -> None:
        self._access_repository.set_user_is_generating_report(user.id, is_generating=True)

        try:
            report_id = self._access_repository.create_new_user_report(user.id)
            report_entity = self._build_report_entity(report_id)

            self._reports_repository.save_user_report(report_entity)
        finally:
            self._access_repository.set_user_is_generating_report(user.id, is_generating=False)

    def _build_report_entity(self, report_id: int) -> ReportGetEntity:
        return (
            ReportsBuilder.from_report_id(report_id)
            .set_messages_count_by_date({datetime.now().date().strftime(DEFAULT_DATE_FORMAT): 23})
            .build()
        )
