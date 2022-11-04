from abc import ABC, abstractmethod

from django.contrib.auth.models import User

from api.domain.entities import GenerateReportEntity


class IGeneratingReportsService(ABC):
    @abstractmethod
    def generate_report(self, generate_report_entity: GenerateReportEntity, user: User) -> None:
        pass
