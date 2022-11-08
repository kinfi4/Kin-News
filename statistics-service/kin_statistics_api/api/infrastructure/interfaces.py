from abc import ABC, abstractmethod

from api.domain.entities import ReportGetEntity
from api.domain.entities.report import ReportIdentificationEntity


class IReportRepository(ABC):
    @abstractmethod
    def save_user_report(self, report: ReportGetEntity) -> None:
        pass

    @abstractmethod
    def get_report(self, report_id: int) -> ReportGetEntity:
        pass

    @abstractmethod
    def get_report_names(self, report_ids: list[int]) -> list[ReportIdentificationEntity]:
        pass

    @abstractmethod
    def update_report_name(self, report_id: int, report_name: str) -> None:
        pass

    @abstractmethod
    def delete_report(self, report_id: int) -> None:
        pass
