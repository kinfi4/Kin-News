import logging

from django.core.exceptions import ObjectDoesNotExist

from api.infrastructure.repositories import UserRepository
from api.exceptions import UsernameAlreadyTakenError, LoginFailedError
from api.domain.entities import UserEntity
from kin_news_core.auth import create_jwt_token


class UserService:
    def __init__(self, user_repository: UserRepository):
        self._repository = user_repository
        self._logger = logging.getLogger(self.__class__.__name__)

    def login(self, user_entity: UserEntity) -> str:
        try:
            user = self._repository.get_user_by_username(user_entity.username)
        except ObjectDoesNotExist:
            raise LoginFailedError(f'Can not find user with specified username and password')

        if not user.check_password(user_entity.password):
            raise LoginFailedError('Specified password is incorrect!')

        return create_jwt_token(user.id)

    def register(self, user: UserEntity) -> str:
        if self._repository.check_if_username_exists(user.username):
            raise UsernameAlreadyTakenError(f'User with {user.username=} already exists, please select another username')

        created_user = self._repository.create_user(user.username, user.password)

        return create_jwt_token(created_user.id)
