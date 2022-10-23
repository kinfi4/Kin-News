from pydantic import ValidationError
from dependency_injector.wiring import inject, Provide
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from api.domain.entities import UserEntity
from api.domain.services import UserService
from api.exceptions import LoginFailedError, UsernameAlreadyTakenError
from config.containers import Container


class LoginView(APIView):
    @inject
    def post(
        self,
        request: Request,
        user_service: UserService = Provide[Container.domain_services.user_service],
    ) -> Response:
        try:
            user_entity = UserEntity(**request.data)
        except ValidationError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error_message': err})

        try:
            token = user_service.login(user_entity)
        except LoginFailedError:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={'error_message': 'Username and/or password are incorrect'}
            )

        return Response(status=status.HTTP_200_OK, data={'token': token})


class RegisterView(APIView):
    @inject
    def post(
        self,
        request: Request,
        user_service: UserService = Provide[Container.domain_services.user_service],
    ) -> Response:
        try:
            user_entity = UserEntity(**request.data)
        except ValidationError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error_message': err})

        try:
            token = user_service.register(user_entity)
        except UsernameAlreadyTakenError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'error_message': 'User with specified username already exists'}
            )

        return Response(status=status.HTTP_201_CREATED, data={'token': token})


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        return Response(status=status.HTTP_200_OK, data={
            "username": request.user.username,
        })
