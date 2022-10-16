import logging

from django.contrib.auth.models import User
from django.db.models import QuerySet

from api.infrastructure.models import Channel


class UserRepository:
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._user_query = User.objects
        self._channel_query = Channel.objects

    def create_user(self, username: str, password: str) -> User:
        self._logger.info('[UserRepository] Creating user')

        return self._user_query.create_user(username=username, password=password)

    def get_user_by_id(self, user_id: int) -> User:
        self._logger.info('[UserRepository] Get user from db by id')

        return self._user_query.get(pk=user_id)

    def get_user_by_username(self, username: str) -> User:
        self._logger.info('[UserRepository] Get user from db by username')

        return self._user_query.get(username=username)

    def check_if_username_exists(self, username: str) -> bool:
        self._logger.info('[UserRepository] Checking if user exists')

        return self._user_query.filter(username=username).exists()

    def get_user_subscriptions(self, user: User) -> QuerySet:
        self._logger.info('[UserRepository] Get user subscriptions from db')

        return self._channel_query.filter(subscribers__username=user.username)
