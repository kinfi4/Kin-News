from datetime import datetime
from typing import Optional

from api.domain.services.reports_generator import IPredictor
from api.tests.factories import telegram_channel_entity
from config.constants import MessageCategories, SentimentTypes
from kin_news_core.telegram import ITelegramProxy
from kin_news_core.telegram.entities import TelegramMessageEntity, TelegramChannelEntity


class FakePredictor(IPredictor):
    def get_sentiment_type(self, text: str, news_type: MessageCategories) -> SentimentTypes:
        return SentimentTypes.POSITIVE

    def get_news_type(self, text: str) -> MessageCategories:
        return MessageCategories.SHELLING


class FakeTelegramClient(ITelegramProxy):
    def download_channel_profile_photo(self, channel_link: str, path_to_save: str) -> None:
        pass

    def fetch_posts_from_channel(
        self,
        channel_name: str,
        *,
        offset_date: Optional[datetime] = None,
        earliest_date: Optional[datetime] = None,
        skip_messages_without_text: bool = False,
    ) -> list[TelegramMessageEntity]:
        pass

    def get_channel(self, channel_link: str) -> TelegramChannelEntity:
        return telegram_channel_entity()
