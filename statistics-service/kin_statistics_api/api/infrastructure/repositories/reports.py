import logging
from typing import Any

from django.contrib.auth.models import User
from django.db.models import Max, F
from pymongo import MongoClient

from api.domain.entities import StatisticalReport, BaseReport, ReportIdentificationEntity, WordCloudReport
from api.exceptions import ReportNotFound, ImpossibleToModifyProcessingReport
from api.models import UserReport, UserGeneratesReport
from api.infrastructure.interfaces import IReportRepository
from config.constants import ReportProcessingResult, ReportTypes


class ReportsMongoRepository(IReportRepository):
    def __init__(self, mongo_client: MongoClient):
        self._mongo_client = mongo_client
        self._reports_db = mongo_client['statistics_service']
        self._reports_collection = self._reports_db['reports']

        self._logger = logging.getLogger(self.__class__.__name__)

    def get_report_names(self, report_ids: list[int]) -> list[ReportIdentificationEntity]:
        dict_reports = self._reports_collection.find(
            {
                "report_id": {"$in": report_ids}
            }
        )

        return [
            self._map_dict_to_identification_entity(report_dict)
            for report_dict in dict_reports
        ]

    def save_user_report(self, report: BaseReport) -> None:
        self._logger.info(f'[ReportsMongoRepository] Saving user report with id: {report.report_id} and status: {report.processing_status}')

        report_dict = report.dict()
        self._reports_collection.replace_one(
            {'report_id': report.report_id},
            report_dict,
            upsert=True,
        )

    def update_report_name(self, report_id: int, report_name: str) -> None:
        report = self.get_report(report_id)

        if report.processing_status == ReportProcessingResult.PROCESSING:
            raise ImpossibleToModifyProcessingReport('You can not change the report during processing.')

        self._reports_collection.update_one(
            {'report_id': report_id},
            {'$set': {'name': report_name}},
        )

    def get_report(self, report_id: int) -> StatisticalReport | WordCloudReport:
        dict_report = self._reports_collection.find_one({
            'report_id': report_id
        })

        if dict_report is None:
            raise ReportNotFound('Report with this id was not found')

        return self._map_dict_to_entity(dict_report)

    def delete_report(self, report_id: int) -> None:
        # try:
        #     report = self.get_report(report_id)
        # except ReportNotFound:
        #     return
        #
        # if report.processing_status == ReportProcessingResult.PROCESSING:
        #     raise ImpossibleToModifyProcessingReport('You can not delete the report during processing.')

        self._reports_collection.delete_one({
            'report_id': report_id
        })

    @staticmethod
    def _map_dict_to_identification_entity(dict_report: dict[str, Any]) -> ReportIdentificationEntity:
        return ReportIdentificationEntity(
            report_id=dict_report['report_id'],
            name=dict_report['name'],
            processing_status=dict_report['processing_status'],
        )

    @staticmethod
    def _map_dict_to_entity(dict_report: dict[str, Any]) -> StatisticalReport | WordCloudReport:
        if dict_report.get('report_type') == ReportTypes.WORD_CLOUD:
            return WordCloudReport.from_dict(dict_report)

        return StatisticalReport.from_dict(dict_report)


class ReportsAccessManagementRepository:
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._user_query = User.objects
        self._user_reports_query = UserReport.objects
        self._user_generating_query = UserGeneratesReport.objects

    def get_user_report_ids(self, user_id: int) -> list[int]:
        user = self._user_query.prefetch_related('reports').get(pk=user_id)

        return list(report.report_id for report in user.reports.all())

    def create_new_user_report(self, user_id: int) -> int:
        """
            Returns: int - Report ID that was created
        """

        last_report_id = (
            self._user_reports_query
            .aggregate(max_report_id=Max(F('report_id')))
            .get('max_report_id', 0)
        )

        if last_report_id is None:
            last_report_id = 0

        self._logger.info(f'Setting report access rights of report_id: {last_report_id + 1} to user: {user_id}')
        self._user_reports_query.create(user_id=user_id, report_id=last_report_id + 1)

        return last_report_id + 1

    def set_user_is_generating_report(self, user_id: int, is_generating: bool) -> None:
        report_generating, _ = self._user_generating_query.get_or_create(user_id=user_id)
        report_generating.report_is_generating = is_generating
        report_generating.save(update_fields=['report_is_generating'])

    def is_report_is_generating(self, user_id: int) -> bool:
        report_generating, _ = self._user_generating_query.get_or_create(user_id=user_id)

        return report_generating.report_is_generating

    def delete_report(self, report_id: int) -> None:
        try:
            self._user_reports_query.get(report_id=report_id).delete()
        except UserReport.DoesNotExist:
            pass
