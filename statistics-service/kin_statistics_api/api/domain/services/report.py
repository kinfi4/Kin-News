from django.contrib.auth.models import User

from api.domain.entities.report import ReportIdentificationEntity, ReportGetEntity, ReportPutEntity
from api.exceptions import ReportAccessForbidden
from api.infrastructure.interfaces import IReportRepository
from api.infrastructure.repositories.reports import ReportsAccessManagementRepository


class ManagingReportsService:
    def __init__(
        self,
        reports_access_management_repository: ReportsAccessManagementRepository,
        reports_repository: IReportRepository,
    ) -> None:
        self._access_management_repository = reports_access_management_repository
        self._reports_repository = reports_repository

    def get_user_repository_names(self, user: User) -> list[ReportIdentificationEntity]:
        user_reports_ids = self._access_management_repository.get_user_report_ids(user.id)

        return self._reports_repository.get_report_names(user_reports_ids)

    def set_report_name(self, user: User, report_put_entity: ReportPutEntity) -> ReportIdentificationEntity:
        self._check_user_access(user, report_ids=[report_put_entity.report_id])

        self._reports_repository.update_report_name(report_put_entity.report_id, report_put_entity.name)

        return ReportIdentificationEntity(
            report_id=report_put_entity.report_id,
            name=report_put_entity.name,
        )

    def get_user_detailed_report(self, user: User, report_id: int) -> ReportGetEntity:
        self._check_user_access(user, report_ids=[report_id])

        return self._reports_repository.get_report(report_id)

    def is_report_is_generating(self, user: User) -> bool:
        return self._access_management_repository.is_report_is_generating(user_id=user.id)

    def _check_user_access(self, user: User, report_ids: list[int]) -> None:
        user_reports = self._access_management_repository.get_user_report_ids(user_id=user.id)

        if not all([report_id in user_reports for report_id in report_ids]):
            raise ReportAccessForbidden(f'User does not have permission for this report!')