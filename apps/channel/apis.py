from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.channel.exceptions import InvalidChannelIdError, InvalidSubscriptionIdError, AlreadyBoughtError
from apps.channel.models import Channel, Membership, Content, Subscription, UserSubscription, UserBoughtContent, \
    ContentType
from apps.channel.serializers import ChannelLeanSerializer, AdminChannelLeanSerializer, MemberChannelLeanSerializer, \
    ChannelInfoSerializer, ChannelContentSerializer, SubscriptionSerializer
from apps.channel_administration.models import ChannelAdmin
from apps.shared import UnauthorizedError, InvalidRequestError
from utils.helpers.bank_helper import BankHelper


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

    def create(self, request, *args, **kwargs):
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


class GetChannelContentFileApi(RetrieveAPIView):
    def retrieve(self, request, content_id, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            raise UnauthorizedError()

        try:
            content = Content.objects.get(id=content_id)
            channel = content.channel
        except Exception as e:
            raise InvalidChannelIdError()

        has_active_subscription = UserSubscription.objects.filter(
            subscription__channel=channel, user=user
        ).exists() and UserSubscription.objects.filter(
            subscription__channel=channel, user=user
        ).first().is_active

        has_bought_content = UserBoughtContent.objects.filter(content=content, user=user).exists()

        user_owner_channels = user.owner_channels.all().values_list("id", flat=True)
        user_admin_channels = user.admin_channels.all().values_list("channel_id", flat=True)

        is_admin = channel.id in user_owner_channels or channel.id in user_admin_channels

        is_free_content = content.free

        if has_active_subscription or has_bought_content or is_free_content or is_admin:

            if content.type == ContentType.text:
                return Response({"text": content.text})
            elif content.type == ContentType.image:
                return Response({"image": content.image})
            elif content.type == ContentType.video:
                return Response({"video": content.video})
            elif content.type == ContentType.voice:
                return Response({"voice": content.voice})

        raise UnauthorizedError()


class CreateSubscriptionApi(CreateAPIView):
    serializer_class = SubscriptionSerializer

    def create(self, request, *args, **kwargs):
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


class GetChannelSubscriptionsApi(RetrieveAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def retrieve(self, request, channel_id, *args, **kwargs):
        try:
            channel = Channel.objects.get(id=channel_id)
        except Exception as e:
            raise InvalidChannelIdError()

        subscriptions = Subscription.objects.filter(channel=channel)
        return Response(self.get_serializer(subscriptions, many=True).data)


class SellSubscriptionApi(RetrieveAPIView):
    def retrieve(self, request, subscription_id, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            raise UnauthorizedError()

        try:
            subscription = Subscription.objects.get(id=subscription_id)
        except:
            raise InvalidSubscriptionIdError()

        if UserSubscription.objects.filter(user=user, subscription=subscription).exists():
            raise AlreadyBoughtError()

        if BankHelper().payment(subscription.price):
            divide_benefit(subscription.price, subscription.channel)

        UserSubscription.objects.create(user=user, subscription=subscription)
        return Response()


class SellContentApi(RetrieveAPIView):
    def retrieve(self, request, content_id, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            raise UnauthorizedError()

        try:
            content = Content.objects.get(id=content_id)
        except:
            raise InvalidSubscriptionIdError()

        if UserBoughtContent.objects.filter(user=user, content=content).exists():
            raise AlreadyBoughtError()

        if BankHelper().payment(content.price):
            divide_benefit(content.price, content.channel)

        UserBoughtContent.objects.create(user=user, content=content)
        return Response()


def divide_benefit(amount, channel):
    remained_amount = (90 / 100) * amount
    for admin in channel.admins.all():
        user = admin.admin
        user_benefit = (admin.percent / 100) * amount
        user.credit += int(user_benefit)
        user.save()
        remained_amount -= (admin.percent / 100) * amount

    channel_creator = channel.creator
    channel_creator.credit += int(remained_amount)
    channel_creator.save()
