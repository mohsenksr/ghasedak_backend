from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.channel.exceptions import InvalidChannelIdError
from apps.channel.models import Channel, Membership, Content, Subscription
from apps.channel.serializers import ChannelLeanSerializer, AdminChannelLeanSerializer, MemberChannelLeanSerializer, \
    ChannelInfoSerializer, ChannelContentSerializer, SubscriptionSerializer
from apps.channel_administration.models import ChannelAdmin
from apps.shared import UnauthorizedError, InvalidRequestError


class GetUserChannelsApi(RetrieveAPIView):
    serializer_class = ChannelLeanSerializer

    def retrieve(self, request, *args, **kwargs):
        owner_channels = Channel.objects.filter(creator=request.user)
        admin_channels = ChannelAdmin.objects.filter(admin=request.user)
        member_channels = Membership.objects.filter(user=request.user)
        owner_channels_data = self.get_serializer(owner_channels, many=True).data
        admin_channels_data = AdminChannelLeanSerializer(admin_channels, many=True).data
        member_channels_data = MemberChannelLeanSerializer(member_channels, many=True).data

        data = {"owner": owner_channels_data, "admin": admin_channels_data, "member": member_channels_data}

        return Response(data, status=status.HTTP_200_OK)


class CreateChannelApi(CreateAPIView):
    serializer_class = ChannelInfoSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            raise UnauthorizedError()
        title = request.data["title"]
        channel_id = request.data["channel_id"]
        bio = request.data["bio"]

        try:
            Channel.objects.create(channel_id=channel_id, title=title, bio=bio, creator=request.user)
            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            raise InvalidChannelIdError()


class JoinChannelApi(RetrieveAPIView):
    def retrieve(self, request, channel_id, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            raise UnauthorizedError()
        try:
            channel = Channel.objects.get(channel_id=channel_id)
            Membership.objects.create(channel=channel, user=user)
            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            raise InvalidChannelIdError()


class GetChannelDescriptionApi(RetrieveAPIView):
    serializer_class = ChannelInfoSerializer

    def retrieve(self, request, channel_id, *args, **kwargs):
        try:
            channel = Channel.objects.get(id=channel_id)
        except Exception as e:
            raise InvalidChannelIdError()

        data = self.get_serializer(channel).data
        return Response(data, status=status.HTTP_200_OK)


class GetChannelContentsApi(RetrieveAPIView):
    serializer_class = ChannelContentSerializer

    def retrieve(self, request, channel_id, *args, **kwargs):
        try:
            channel = Channel.objects.get(id=channel_id)
        except Exception as e:
            raise InvalidChannelIdError()

        contents = Content.objects.filter(channel_id=channel_id)
        data = self.get_serializer(contents, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class CreateSubscriptionApi(CreateAPIView):
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            raise UnauthorizedError()

        try:
            channel_id = int(request.data["channel_id"])
            duration = request.data["duration"]
            price = int(request.data["price"])
        except:
            raise InvalidRequestError()

        try:
            channel = Channel.objects.get(id=channel_id)
        except:
            raise InvalidChannelIdError()

        if channel.creator != request.user:
            raise UnauthorizedError()

        try:
            print("ok")
            Subscription.objects.create(channel=channel, duration=duration, price=price)
            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            raise InvalidChannelIdError()


class ChannelSubscriptionsApi(RetrieveAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def retrieve(self, request, channel_id, *args, **kwargs):
        try:
            channel = Channel.objects.get(id=channel_id)
        except Exception as e:
            raise InvalidChannelIdError()

        subscriptions = Subscription.objects.filter(channel=channel)
        return Response(self.get_serializer(subscriptions, many=True).data)
