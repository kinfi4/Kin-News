import logging

from api.domain.entities import GenerateReportEntity, WordCloudReport
from api.domain.services import IGeneratingReportsService
from api.domain.services.reports_generator.predictor.predictor import Predictor
from api.infrastructure.interfaces import IReportRepository
from api.infrastructure.repositories import ReportsAccessManagementRepository
from kin_news_core.telegram import ITelegramProxy


class GenerateWordCloudReportService(IGeneratingReportsService):
    def __init__(
        self,
        telegram_client: ITelegramProxy,
        reports_repository: IReportRepository,
        report_access_repository: ReportsAccessManagementRepository,
        predictor: Predictor,
    ) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)
        self._telegram = telegram_client
        self._reports_repository = reports_repository
        self._access_repository = report_access_repository
        self._predictor = predictor

    def generate_report(self, generate_report_entity: GenerateReportEntity, user_id: int) -> WordCloudReport:
        self._logger.info(f'[GenerateStatisticalReportService] Starting generating report for user: {user_id}')

        self._access_repository.set_user_is_generating_report(user_id, is_generating=True)
        report_id = self._access_repository.create_new_user_report(user_id)

        empty_report = self._build_empty_report(report_id)
        self._reports_repository.save_user_report(empty_report)

        try:
            report_entity = self._build_report_entity(report_id, generate_report_entity)

            self._reports_repository.save_user_report(report_entity)

            return report_entity
        except Exception as error:
            self._logger.error(
                f'[GenerateStatisticalReportService] {error.__class__.__name__} occurred during processing report for user: {user_id} with message: {str(error)}'
            )

            postponed_report = self._build_processing_failed_entity(report_id, error)
            self._reports_repository.save_user_report(postponed_report)
        finally:
            self._access_repository.set_user_is_generating_report(user_id, is_generating=False)

    def _build_report_entity(self, report_id: int, generate_report_entity: GenerateReportEntity) -> WordCloudReport:
        pass

    def _build_empty_report(self, report_id: int) -> WordCloudReport:
        pass

    def _build_postponed_report(self, report_id: int) -> WordCloudReport:
        pass
