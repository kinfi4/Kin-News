from pydantic import ValidationError
from dependency_injector.wiring import inject, Provide
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from api.domain.services import ChannelService
from api.domain.entities import ChannelPostEntity
from config.containers import Container


class ChannelListView(APIView):
    permission_classes = (IsAuthenticated,)

    @inject
    def get(
        self,
        request: Request,
        channel_service: ChannelService = Provide[Container.services.channel_service],
    ) -> Response:
        channels = channel_service.get_user_channels(request.user)
        channels_serialized = [channel.dict() for channel in channels]

        return Response(data=channels_serialized)

    @inject
    def post(
        self,
        request: Request,
        channel_service: ChannelService = Provide[Container.services.channel_service],
    ) -> Response:
        try:
            channels_entity = ChannelPostEntity(**request.data)
        except ValidationError as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error_message': err})

        channel = channel_service.subscribe_user(request.user, channels_entity)

        return Response(data=channel.dict())
