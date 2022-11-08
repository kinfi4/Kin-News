import logging
from datetime import datetime, timedelta
from typing import Optional

from api.domain.entities import ChannelGetEntity
from api.domain.entities.message import MessageGetEntity
from kin_news_core.exceptions import InvalidChannelURLError
from kin_news_core.telegram import ITelegramProxy


class MessageService:
    def __init__(self, telegram_client: ITelegramProxy):
        self._telegram_client = telegram_client
        self._logger = logging.getLogger(self.__class__.__name__)

    def get_user_posts(
        self,
        user_channels: list[ChannelGetEntity],
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> list[MessageGetEntity]:
        if end_time is None:
            end_time = datetime.now()

        if start_time is None:
            start_time = datetime.now() - timedelta(hours=5)

        messages = []
        for channel in user_channels:
            self._logger.info(f'Fetching messages for {channel.link}')

            try:
                channel_messages = self._telegram_client.fetch_posts_from_channel(channel.link, offset_date=end_time, earliest_date=start_time)
            except InvalidChannelURLError:
                continue  # if the channel has changed it's url, we just skip it

            messages.extend([MessageGetEntity.from_tg_entity(c) for c in channel_messages])

        self._logger.info(f'Total messages found for period: {start_time}:{end_time} is {len(messages)}')

        return self._sort_messages_by_time(messages)

    @staticmethod
    def _sort_messages_by_time(messages: list[MessageGetEntity]) -> list[MessageGetEntity]:
        return sorted(messages, key=lambda m: m.created_at)
