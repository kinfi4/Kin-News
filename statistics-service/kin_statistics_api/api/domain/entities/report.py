from typing import Optional

from pydantic import BaseModel, Field, validator, ValidationError

from config.constants import MessageCategories, ReportProcessingResult


class ReportGetEntity(BaseModel):
    report_id: int
    name: str
    processing_status: ReportProcessingResult = Field(..., alias='processingStatus')

    report_failed_reason: Optional[str] = Field(None, alias='reportFailedReason')

    total_messages_count: Optional[int] = Field(None, alias='totalMessagesCount')

    messages_count_by_channel: Optional[dict[str, int]] = Field(None, alias='messagesCountByChannel')
    messages_count_by_date: Optional[dict[str, int]] = Field(None, alias='messagesCountByDate')
    messages_count_by_day_hour: Optional[dict[str, int]] = Field(None, alias='messagesCountByDayHour')
    messages_count_by_category: Optional[dict[MessageCategories, int]] = Field(None, alias='messagesCountByCategory')

    @validator('messages_count_by_day_hour', pre=True)
    def _validate_day_hour(cls, messages_dict: dict[str, int]):
        if len(messages_dict) != 24:
            raise ValidationError(f'Invalid format for messagesCountByDayHour field')

        if any([int(n) not in range(24) for n in messages_dict.keys()]):  # all hours must be between 0 and 23
            raise ValidationError(f'Invalid format for messagesCountByDayHour field')

        return messages_dict

    class Config:
        allow_population_by_field_name = True


class ReportPutEntity(BaseModel):
    name: str
    report_id: int


class ReportIdentificationEntity(BaseModel):
    report_id: int
    name: str
