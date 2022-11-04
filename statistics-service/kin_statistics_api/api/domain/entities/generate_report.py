from datetime import date, datetime
from typing import Union

from django.conf import settings
from pydantic import BaseModel, validator, ValidationError, Field

from config.constants import DEFAULT_DATE_FORMAT


def _cast_string_to_date(date_string: str) -> date:
    try:
        return datetime.strptime(date_string, DEFAULT_DATE_FORMAT).date()
    except ValueError:
        raise ValidationError(f'Invalid string format for incoming StartDate field!')


class GenerateReportEntity(BaseModel):
    start_date: date = Field(..., alias='startDate')
    end_date: date = Field(..., alias='endDate')
    channel_list: list[str] = Field(..., alias='channels')

    @validator('channel_list', pre=True)
    def validate_channels(cls, channels: list[str]) -> list[str]:
        if len(channels) > settings.MAX_SUBSCRIPTIONS_ALLOWED or not channels:
            raise ValidationError(f'You passed invalid list of channels to process!')

        return channels

    @validator('start_date', pre=True)
    def validate_and_cast_start_date(cls, value: Union[str, date]):
        if isinstance(value, str):
            return _cast_string_to_date(value)

        return value  # validation for correct date will be later

    @validator('end_date', pre=True)
    def validate_and_cast_end_date(cls, value: Union[str, date]):
        if isinstance(value, str):
            return _cast_string_to_date(value)

        return value  # validation for correct date will be later

    class Config:
        allow_population_by_field_name = True


# {"startDate":"03/03/2002", "endDate": "03/05/2003", "channels": ["some-name"]}
