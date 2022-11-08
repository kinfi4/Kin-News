import logging
from datetime import datetime, date
from typing import Union, Any

from api.domain.services.reports_generator import IGeneratingReportsService
from api.domain.services.reports_generator.predictor.predictor import Predictor
from api.infrastructure.repositories import IReportRepository, ReportsAccessManagementRepository
from api.domain.entities import GenerateReportEntity, ReportGetEntity
from api.domain.services.reports_generator.reports_builder import ReportsBuilder
from kin_news_core.telegram.interfaces import ITelegramProxy
from config.constants import DEFAULT_DATE_FORMAT, ReportProcessingResult, MessageCategories, SentimentTypes


class GeneratingReportsService(IGeneratingReportsService):
    def __init__(
        self,
        telegram_client: ITelegramProxy,
        reports_repository: IReportRepository,
        report_access_repository: ReportsAccessManagementRepository,
        predictor: Predictor,
    ) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)
        self._telegram = telegram_client
        self._reports_repository = reports_repository
        self._access_repository = report_access_repository
        self._predictor = predictor

    def generate_report(self, generate_report_entity: GenerateReportEntity, user_id: int) -> None:
        self._logger.info(f'[GeneratingReportsService] Starting generating report for user: {user_id}')

        self._access_repository.set_user_is_generating_report(user_id, is_generating=True)
        report_id = self._access_repository.create_new_user_report(user_id)

        try:
            report_entity = self._build_report_entity(report_id, generate_report_entity)

            self._reports_repository.save_user_report(report_entity)
        except Exception as error:
            self._logger.error(
                f'[GeneratingReportsService] {error.__class__.__name__} occurred during processing report for user: {user_id} with message: {str(error)}'
            )

            postponed_report = self._build_processing_failed_entity(report_id, error)
            self._reports_repository.save_user_report(postponed_report)
        finally:
            self._access_repository.set_user_is_generating_report(user_id, is_generating=False)

    def _build_report_entity(self, report_id: int, generate_report_entity: GenerateReportEntity) -> ReportGetEntity:
        report_data = self._gather_report_data(generate_report_entity)

        return (
            ReportsBuilder.from_report_id(report_id)
            .set_messages_count_by_day_hour(report_data['messages_count_by_day_hour'])
            .set_messages_count_by_category(report_data['messages_count_by_category'])
            .set_messages_count_by_channel(report_data['messages_count_by_channel'])
            .set_messages_count_by_date(report_data['messages_count_by_date'])
            .set_messages_count_by_date_by_category(report_data['messages_count_by_date_by_category'])
            .set_messages_count_by_channel_by_category(report_data['messages_count_by_channel_by_category'])
            .set_messages_count_by_sentiment_type(report_data['messages_count_by_sentiment_type'])
            .set_messages_count_by_channel_by_sentiment_type(report_data['messages_count_by_channel_sentiment_type'])
            .set_messages_count_by_date_by_sentiment_type(report_data['messages_count_by_date_by_sentiment_type'])
            .build()
        )

    @staticmethod
    def _build_processing_failed_entity(report_id: int, error: Exception) -> ReportGetEntity:
        return (
            ReportsBuilder.from_report_id(report_id)
            .set_status(ReportProcessingResult.POSTPONED)
            .set_failed_reason(str(error))
            .build()
        )

    def _gather_report_data(self, generate_entity: GenerateReportEntity) -> dict[Union[str, MessageCategories], Any]:
        report_data = self._initialize_report_date_dict(generate_entity)

        for channel in generate_entity.channel_list:
            telegram_messages = self._telegram.fetch_posts_from_channel(
                channel_name=channel,
                offset_date=self._datetime_from_date(generate_entity.end_date),
                earliest_date=self._datetime_from_date(generate_entity.start_date),
                skip_messages_without_text=True,
            )

            self._logger.info(f'[GeneratingReportsService] Gathered {len(telegram_messages)} messages from {channel}')

            for message in telegram_messages:

                message_date_str = message.created_at.date().strftime(DEFAULT_DATE_FORMAT)
                message_hour = message.created_at.hour

                message_category = self._predictor.get_news_type(message.text)
                message_sentiment_category = self._predictor.get_sentiment_type(
                    message.text,
                    news_type=message_category,
                    make_preprocessing=True,
                )

                report_data['total_messages'] += 1
                report_data['messages_count_by_channel'][channel] += 1
                report_data['messages_count_by_day_hour'][str(message_hour)] += 1
                report_data['messages_count_by_category'][message_category] += 1
                report_data['message_count_by_sentiment'][message_sentiment_category] += 1

                if message_date_str not in report_data['messages_count_by_date']:
                    report_data['messages_count_by_date'][message_date_str] = 0

                report_data['messages_count_by_date'][message_date_str] += 1

                if message_date_str not in report_data['messages_count_by_date_by_category']:
                    report_data['messages_count_by_date_by_category'][message_date_str] = {
                        category: 0 for category in MessageCategories
                    }

                report_data['messages_count_by_date_by_category'][message_date_str][message_category] += 1

                report_data['messages_count_by_channel_by_category'][channel][message_category] += 1
                report_data['messages_count_by_sentiment_type'][message_sentiment_category] += 1
                report_data['messages_count_by_channel_sentiment_type'][channel][message_sentiment_category] += 1

                if message_date_str not in report_data['messages_count_by_date_by_sentiment_type']:
                    report_data['messages_count_by_date_by_sentiment_type'][message_date_str] = {
                        sentiment_type: 0 for sentiment_type in SentimentTypes
                    }

                report_data['messages_count_by_date_by_sentiment_type'][message_date_str][message_sentiment_category] += 1

        return report_data

    @staticmethod
    def _datetime_from_date(dt: date) -> datetime:
        return datetime(
            year=dt.year,
            month=dt.month,
            day=dt.day,
        )

    @staticmethod
    def _initialize_report_date_dict(generate_entity: GenerateReportEntity) -> dict[Union[str, MessageCategories], Any]:
        return {
            'total_messages': 0,
            'messages_count_by_channel': {
                channel: 0 for channel in generate_entity.channel_list
            },
            'messages_count_by_date': {},
            'messages_count_by_day_hour': {
                str(hour): 0 for hour in range(24)
            },
            'messages_count_by_category': {
                category: 0 for category in MessageCategories
            },
            'message_count_by_sentiment': {
                SentimentTypes.NEUTRAL: 0,
                SentimentTypes.POSITIVE: 0,
                SentimentTypes.NEGATIVE: 0,
            },
            'messages_count_by_date_by_category': {},
            'messages_count_by_channel_by_category': {
                channel: {
                    category: 0 for category in MessageCategories
                }
                for channel in generate_entity.channel_list
            },
            'messages_count_by_sentiment_type': {sentiment_type: 0 for sentiment_type in SentimentTypes},
            'messages_count_by_channel_sentiment_type': {
                channel: {
                    sentiment_type: 0 for sentiment_type in SentimentTypes
                }
                for channel in generate_entity.channel_list
            },
            'messages_count_by_date_by_sentiment_type': {},
        }
