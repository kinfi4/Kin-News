from typing import Optional
from datetime import datetime

from dependency_injector.wiring import inject, Provide
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from api.exceptions import InvalidURIParams
from api.domain.services import MessageService, ChannelService
from config.containers import Container
from kin_news_core.auth import JWTAuthentication


class MessagesView(APIView):
    authentication_classes = (SessionAuthentication, JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @inject
    def get(
        self,
        request: Request,
        message_service: MessageService = Provide[Container.domain_services.message_service],
        channel_service: ChannelService = Provide[Container.domain_services.channel_service],
    ) -> Response:

        try:
            start_time, end_time = self._parse_query_params(request)
            user_channels = channel_service.get_user_channels(request.user)

            messages = message_service.get_user_posts(user_channels, start_time=start_time, end_time=end_time)
        except InvalidURIParams as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error_message': str(err)})

        messages_serialized = [message.dict(by_alias=True) for message in messages]
        return Response(data={
            'messages': messages_serialized,
            'messagesCount': len(messages_serialized),
        })

    @staticmethod
    def _parse_query_params(request: Request) -> tuple[Optional[datetime], Optional[datetime]]:
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        try:
            if start_time is not None:
                start_time = datetime.fromtimestamp(int(start_time))

            if end_time is not None:
                end_time = datetime.fromtimestamp(int(end_time))

            if start_time > end_time:
                raise InvalidURIParams(f'Start time must be earlier than end time.')

            if (end_time - start_time).total_seconds() > 3600 * 24:
                raise InvalidURIParams(f'You can not fetch data for such long period of time!')
        except ValueError:
            raise InvalidURIParams(f'You have passed invalid query params! Offset/End time must be integers representing timestamp')

        return start_time, end_time
