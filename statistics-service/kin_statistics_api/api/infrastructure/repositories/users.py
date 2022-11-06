from django.contrib.auth.models import User

from api.models import UserGeneratesReport


class UserRepository:
    def __init__(self):
        self._user_query = User.objects
        self._user_generates_report_query = UserGeneratesReport.objects

    def check_if_username_exists(self, username: str) -> bool:
        return self._user_query.filter(username=username).exists()

    def create_user_by_username(self, username: str) -> None:
        self._user_query.create_user(username=username)

    def is_user_report_generating(self, user_id: int) -> bool:
        return self._user_generates_report_query.get(user_id=user_id).report_is_generating
