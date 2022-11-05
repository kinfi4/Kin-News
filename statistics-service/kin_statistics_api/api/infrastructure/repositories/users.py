from django.contrib.auth.models import User


class UserRepository:
    def __init__(self):
        self._user_query = User.objects

    def check_if_username_exists(self, username: str) -> bool:
        return self._user_query.filter(username=username).exists()

    def create_user_by_username(self, username: str) -> None:
        self._user_query.create_user(username=username)
