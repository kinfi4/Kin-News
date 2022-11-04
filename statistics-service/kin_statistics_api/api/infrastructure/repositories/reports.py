from typing import Any

from django.contrib.auth.models import User
from django.db.models import Max, F
from pymongo import MongoClient

from api.domain.entities import ReportGetEntity
from api.models import UserReport, UserGeneratesReport
from api.domain.entities.report import ReportIdentificationEntity
from api.infrastructure.interfaces import IReportRepository


class ReportsMongoRepository(IReportRepository):
    def __init__(self, mongo_client: MongoClient):
        self._mongo_client = mongo_client
        self._reports_db = mongo_client['statistics_service']
        self._reports_collection = self._reports_db['reports']

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

    def save_user_report(self, report: ReportGetEntity) -> None:
        report_dict = report.dict()
        self._reports_collection.insert_one(report_dict)

    def update_report_name(self, report_id: int, report_name: str) -> None:
        self._reports_collection.update_one(
            {'report_id': report_id},
            {'$set': {'name': report_name}},
        )

    def get_report(self, report_id: int) -> ReportGetEntity:
        dict_report = self._reports_collection.find_one(
            {
                'report_id': report_id
            }
        )

        return self._map_dict_to_entity(dict_report)

    @staticmethod
    def _map_dict_to_identification_entity(dict_report: dict[str, Any]) -> ReportIdentificationEntity:
        return ReportIdentificationEntity(
            report_id=dict_report['report_id'],
            name=dict_report['name'],
        )

    @staticmethod
    def _map_dict_to_entity(dict_report: dict[str, Any]) -> ReportGetEntity:
        return ReportGetEntity(
            report_id=dict_report['report_id'],
            name=dict_report['name'],
            total_messages_count=dict_report['total_messages_count'],
            messages_count_by_channel=dict_report['messages_count_by_channel'],
            messages_count_by_date=dict_report['messages_count_by_date'],
            messages_count_by_day_hour=dict_report['messages_count_by_day_hour'],
            messages_count_by_category=dict_report['messages_count_by_category'],
        )


class ReportsAccessManagementRepository:
    def __init__(self):
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

        self._user_reports_query.create(user_id=user_id, report_id=last_report_id + 1)

        return last_report_id + 1

    def set_user_is_generating_report(self, user_id: int, is_generating: bool) -> None:
        report_generating, _ = self._user_generating_query.get_or_create(user_id=user_id)
        report_generating.report_is_generating = is_generating
        report_generating.save(update_fields=['report_is_generating'])

    def is_report_is_generating(self, user_id: int) -> bool:
        report_generating, _ = self._user_generating_query.get_or_create(user_id=user_id)

        return report_generating.report_is_generating
