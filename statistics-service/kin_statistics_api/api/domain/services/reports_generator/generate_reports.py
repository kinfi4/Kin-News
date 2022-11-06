import logging
from datetime import datetime

from api.domain.services.reports_generator import IGeneratingReportsService
from api.infrastructure.repositories import IReportRepository, ReportsAccessManagementRepository
from api.domain.entities import GenerateReportEntity, ReportGetEntity
from api.domain.services.reports_generator.reports_builder import ReportsBuilder
from kin_news_core.telegram.interfaces import ITelegramProxy
from config.constants import DEFAULT_DATE_FORMAT, ReportProcessingResult


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

    def generate_report(self, generate_report_entity: GenerateReportEntity, user_id: int) -> None:
        self._logger.info(f'[GeneratingReportsService] Starting generating report for user: {user_id}')

        self._access_repository.set_user_is_generating_report(user_id, is_generating=True)
        report_id = self._access_repository.create_new_user_report(user_id)

        try:
            report_entity = self._build_report_entity(report_id)

            self._reports_repository.save_user_report(report_entity)
        except Exception as error:
            self._logger.error(
                f'[GeneratingReportsService] {error.__class__.__name__} occurred during processing report for user: {user_id} with message: {str(error)}'
            )
            postponed_report = self._build_processing_failed_entity(report_id, error)
            self._reports_repository.save_user_report(postponed_report)
        finally:
            self._access_repository.set_user_is_generating_report(user_id, is_generating=False)

    def _build_report_entity(self, report_id: int) -> ReportGetEntity:
        return (
            ReportsBuilder.from_report_id(report_id)
            .set_messages_count_by_date({datetime.now().date().strftime(DEFAULT_DATE_FORMAT): 23})
            .build()
        )

    @staticmethod
    def _build_processing_failed_entity(report_id: int, error: Exception) -> ReportGetEntity:
        return (
            ReportsBuilder.from_report_id(report_id)
            .set_status(ReportProcessingResult.POSTPONED)
            .set_failed_reason(str(error))
            .build()
        )
