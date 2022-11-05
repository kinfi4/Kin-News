from api.exceptions import UsernameTaken
from api.infrastructure.repositories import UserRepository
from api.domain.entities import CreateUserEntity


class UserService:
    def __init__(self, access_repository: UserRepository):
        self._access_repository = access_repository

    def register_user(self, create_user_entity: CreateUserEntity) -> None:
        if self._access_repository.check_if_username_exists(create_user_entity.username):
            raise UsernameTaken('User with this username already exists')

        self._access_repository.create_user_by_username(create_user_entity.username)
