from rest_framework.generics import CreateAPIView, RetrieveAPIView

from rest_framework.response import Response
from rest_framework import status
from apps.account.models import User
from apps.channel.exceptions import InvalidChannelIdError
from apps.channel.models import Channel
from apps.channel_administration.exceptions import InvalidAdminIdError, InvalidPercentError
from apps.channel_administration.models import ChannelAdmin
from apps.channel_administration.serializers import CreateAdminSerializer
from apps.shared import UnauthorizedError, InvalidRequestError


class CreateAdminApi(CreateAPIView):
    serializer_class = CreateAdminSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            raise UnauthorizedError()

        try:
            channel_id = int(request.data["channel_id"])
            admin_username = request.data["admin_username"]
            percent = int(request.data["percent"])
        except:
            raise InvalidRequestError()

        try:
            channel = Channel.objects.get(id=channel_id)
        except:
            raise InvalidChannelIdError()

        try:
            admin = User.objects.get(username=admin_username)
        except:
            raise InvalidAdminIdError()

        if channel.creator != request.user:
            raise UnauthorizedError()

        if channel.sum_admin_percents + percent > 100:
            raise InvalidPercentError()

        try:
            print("ok")
            ChannelAdmin.objects.create(channel=channel, admin=admin, percent=percent)
            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            raise InvalidChannelIdError()
