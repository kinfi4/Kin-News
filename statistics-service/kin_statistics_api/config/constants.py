from enum import Enum


class MessageCategories(str, Enum):
    POLITICAL = 'Political'
    SHELLING = 'Shelling'
    HUMANITARIAN = 'Humanitarian'
    ECONOMICAL = 'Economical'


DEFAULT_DATE_FORMAT = '%d/%m/%Y'


class ReportProcessingResult(str, Enum):
    POSTPONED = 'Postponed'
    READY = 'Ready'
