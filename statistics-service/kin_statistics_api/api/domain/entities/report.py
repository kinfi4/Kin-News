from typing import Optional
from collections import Counter

from pydantic import BaseModel, Field, validator, ValidationError

from config.constants import MessageCategories, ReportProcessingResult, SentimentTypes, ReportTypes


class BaseReport(BaseModel):
    report_id: int = Field(..., alias='reportId')
    name: str = Field(max_length=80)
    report_type: ReportTypes = Field(ReportTypes.STATISTICAL, alias='reportType')
    processing_status: ReportProcessingResult = Field(..., alias='processingStatus')

    report_failed_reason: Optional[str] = Field(None, alias='reportFailedReason')


class StatisticalReport(BaseReport):
    total_messages_count: Optional[int] = Field(None, alias='totalMessagesCount')

    messages_count_by_channel: Optional[dict[str, int]] = Field(None, alias='messagesCountByChannel')
    messages_count_by_date: Optional[dict[str, int]] = Field(None, alias='messagesCountByDate')
    messages_count_by_day_hour: Optional[dict[str, int]] = Field(None, alias='messagesCountByDayHour')
    messages_count_by_category: Optional[dict[MessageCategories, int]] = Field(None, alias='messagesCountByCategory')

    messages_count_by_date_by_category: Optional[dict[str, dict[MessageCategories, int]]] = Field(
        None,
        alias='messagesCountByDateByCategory',
    )

    messages_count_by_channel_by_category: Optional[dict[str, dict[MessageCategories, int]]] = Field(
        None,
        alias='messagesCountByChannelByCategory',
    )

    messages_count_by_sentiment_type: Optional[dict[SentimentTypes, int]] = Field(
        None,
        alias='messagesCountBySentimentType',
    )

    messages_count_by_channel_by_sentiment_type: Optional[dict[str, dict[SentimentTypes, int]]] = Field(
        None,
        alias='messagesCountByChannelBySentimentType',
    )
    messages_count_by_date_by_sentiment_type: Optional[dict[str, dict[SentimentTypes, int]]] = Field(
        None,
        alias='messagesCountByDateBySentimentType',
    )

    @validator('messages_count_by_day_hour', pre=True)
    def _validate_day_hour(cls, messages_dict: dict[str, int]):
        if len(messages_dict) != 24:
            raise ValidationError(f'Invalid format for messagesCountByDayHour field')

        if any([int(n) not in range(24) for n in messages_dict.keys()]):  # all hours must be between 0 and 23
            raise ValidationError(f'Invalid format for messagesCountByDayHour field')

        return messages_dict

    class Config:
        allow_population_by_field_name = True


class WordCloudReport(BaseReport):
    total_words: Optional[int] = Field(None, alias='totalWords')
    total_words_frequency: Optional[list[tuple[str, int]]] = Field(None, alias='totalWordsFrequency')
    data_by_channel: Optional[dict[str, list[tuple[str, int]]]] = Field(None, alias='dataByChannel')

    data_by_category: Optional[
        dict[SentimentTypes | MessageCategories, list[tuple[str, int]]]
    ] = Field(None, alias='dataByCategory')

    data_by_channel_by_category: Optional[
        dict[str, dict[SentimentTypes | MessageCategories, list[tuple[str, int]]]]
    ] = Field(None, alias='dataByChannelByCategory')

    class Config:
        allow_population_by_field_name = True


class ReportPutEntity(BaseModel):
    name: str = Field(max_length=80)
    report_id: int = Field(..., alias='reportId')

    class Config:
        allow_population_by_field_name = True


class ReportIdentificationEntity(BaseModel):
    processing_status: ReportProcessingResult = Field(ReportProcessingResult.READY, alias='processingStatus')
    report_id: int = Field(..., alias='reportId')
    name: str

    class Config:
        allow_population_by_field_name = True
