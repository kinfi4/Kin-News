from pydantic import ValidationError
from dependency_injector.wiring import inject, Provide
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from api.domain.services import ChannelService
from api.domain.entities import ChannelPostEntity
from api.exceptions import UserIsNotSubscribed
from config.containers import Container
from kin_news_core.exceptions import InvalidChannelURLError


class ChannelListView(APIView):
    permission_classes = (IsAuthenticated,)

    @inject
    def get(
        self,
        request: Request,
        channel_service: ChannelService = Provide[Container.domain_services.channel_service],
    ) -> Response:
        channels = channel_service.get_user_channels(request.user)
        channels_serialized = [channel.dict(by_alias=True) for channel in channels]

        return Response(data=channels_serialized)

    @inject
    def post(
        self,
        request: Request,
        channel_service: ChannelService = Provide[Container.domain_services.channel_service],
    ) -> Response:
        try:
            channels_entity = ChannelPostEntity(**request.data)
            channel = channel_service.subscribe_user(request.user, channels_entity)
        except ValidationError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error_message': str(err)})
        except InvalidChannelURLError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error_message': str(err)})

        return Response(data=channel.dict(by_alias=True))


class ChannelUnsubscribeView(APIView):
    permission_classes = (IsAuthenticated,)

    @inject
    def delete(
        self,
        request: Request,
        channel: str,
        channel_service: ChannelService = Provide[Container.domain_services.channel_service],
    ) -> Response:
        try:
            channels_entity = ChannelPostEntity(link=channel)
            channel_service.unsubscribe_channel(request.user, channel_post_entity=channels_entity)
        except ValidationError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error_message': str(err)})
        except UserIsNotSubscribed as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error_message': str(err)})

        return Response(status=status.HTTP_204_NO_CONTENT)
