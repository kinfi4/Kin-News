from abc import ABC, abstractmethod

from api.domain.entities import GenerateReportEntity


class IGeneratingReportsService(ABC):
    @abstractmethod
    def generate_report(self, generate_report_entity: GenerateReportEntity, user_id: int) -> None:
        pass
