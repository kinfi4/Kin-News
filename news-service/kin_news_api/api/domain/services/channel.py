import logging

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from api.domain.entities import ChannelGetEntity, ChannelPostEntity
from api.exceptions import UserIsNotSubscribed
from api.infrastructure.repositories import ChannelRepository, UserRepository
from kin_news_core.telegram.interfaces import ITelegramProxy
from kin_news_core.telegram.entities import ChannelEntity
from kin_news_core.exceptions import InvalidChannelURLError
from kin_news_core.cache import AbstractCache


class ChannelService:
    def __init__(
        self,
        channel_repository: ChannelRepository,
        user_repository: UserRepository,
        telegram_client: ITelegramProxy,
        cache_client: AbstractCache,
    ) -> None:
        self._channel_repository = channel_repository
        self._user_repository = user_repository
        self._telegram_client = telegram_client
        self._cache_client = cache_client
        self._logger = logging.getLogger(self.__class__.__name__)

    def unsubscribe_channel(self, user: User, channel_post_entity: ChannelPostEntity) -> None:
        try:
            self._channel_repository.unsubscribe_user(user, channel_link=channel_post_entity.link)
        except ObjectDoesNotExist:
            raise UserIsNotSubscribed(f'You are not subscribed to {channel_post_entity.link}')

    def subscribe_user(self, user: User, channel_post_entity: ChannelPostEntity) -> ChannelGetEntity:
        channel_entity = self._get_channel_entity(channel_post_entity.link)
        profile_url = self._get_channel_profile_photo_url(channel_post_entity.link)

        channel = self._channel_repository.get_channel_by_link(channel_entity.link)
        self._channel_repository.add_channel_subscriber(channel, user)

        return ChannelGetEntity(**channel_entity.dict(), profile_photo_url=profile_url)

    def get_user_channels(self, user: User) -> list[ChannelGetEntity]:
        orm_channels = self._user_repository.get_user_subscriptions(user)

        channels: list[ChannelGetEntity] = []
        for orm_channel in orm_channels:
            try:
                channel_telegram_entity = self._get_channel_entity(orm_channel.link)
                channel_entity = ChannelGetEntity(
                    **channel_telegram_entity.dict()
                )

                channels.append(channel_entity)
            except InvalidChannelURLError:
                channels.append(self._build_deleted_channel_entity(orm_channel.link))

        return channels

    def _get_channel_entity(self, channel_link: str) -> ChannelEntity:
        channel_entity = self._cache_client.get_channel_info(channel_link)

        if channel_entity is None:
            channel_entity = self._telegram_client.get_channel(channel_link)
            self._cache_client.set_channel_info(channel_entity)

        return channel_entity

    def _get_channel_profile_photo_url(self, channel_link: str) -> str:
        # redis integration

        return ''

    @staticmethod
    def _build_deleted_channel_entity(link: str) -> ChannelGetEntity:
        return ChannelGetEntity(
            link=link,
            title='This Channel was deleted, or channel link has changed',
            description='',
            participants_count='0 K',
        )
