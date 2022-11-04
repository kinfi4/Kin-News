from enum import Enum


class MessageCategories(str, Enum):
    POLITICAL = 'Political'
    SHELLING = 'Shelling'
    HUMANITARIAN = 'Humanitarian'
    ECONOMICAL = 'Economical'


DEFAULT_DATE_FORMAT = '%d/%m/%Y'
