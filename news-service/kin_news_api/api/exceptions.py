class KinNewsBaseException(Exception):
    pass


class BaseAuthError(KinNewsBaseException):
    pass


class UsernameAlreadyTakenError(BaseAuthError):
    pass


class LoginFailedError(BaseAuthError):
    pass


class UserIsNotSubscribed(KinNewsBaseException):
    pass


class ChannelDoesNotExists(KinNewsBaseException):
    pass
