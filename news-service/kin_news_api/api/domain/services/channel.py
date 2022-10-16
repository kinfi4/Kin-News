import logging

from django.contrib.auth.models import User

from api.domain.entities.channel import ChannelPostEntity, ChannelGetEntity
from api.infrastructure.repositories import ChannelRepository, UserRepository


class ChannelService:
    def __init__(self, channel_repository: ChannelRepository, user_repository: UserRepository):
        self._channel_repository = channel_repository
        self._user_repository = user_repository
        self._logger = logging.getLogger(self.__class__.__name__)

    def subscribe_user(self, user: User, channel_entity: ChannelPostEntity) -> ChannelGetEntity:
        channel = self._channel_repository.get_channel_by_link(channel_entity.link)
        self._channel_repository.add_channel_subscriber(channel, user)

        return ChannelGetEntity(link=channel.link, display_name='something')

    def get_user_channels(self, user: User) -> list[ChannelGetEntity]:
        orm_channels = self._user_repository.get_user_subscriptions(user)

        return [
            ChannelGetEntity(link=c.link, display_name='something') for c in orm_channels
        ]
