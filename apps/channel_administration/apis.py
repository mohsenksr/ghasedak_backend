import os

from rest_framework.generics import CreateAPIView, RetrieveAPIView

from rest_framework.response import Response
from rest_framework import status
from apps.account.models import User
from apps.channel.exceptions import InvalidChannelIdError, InvalidContentIdError, InappropriateApiError
from apps.channel.models import Channel, Subscription, Membership, Content, ContentType
from apps.channel.serializers import SubscriptionSerializer, MemberUserSerializer, ChannelContentSerializer
from apps.channel_administration.exceptions import InvalidAdminIdError, InvalidPercentError, EmptyBalanceError, \
    IncompleteProfileError
from apps.channel_administration.models import ChannelAdmin
from apps.channel_administration.serializers import AdminSerializer
from apps.shared import UnauthorizedError, InvalidRequestError
from utils.helpers.bank_helper import BankHelper
from django.utils.html import escape


class CreateAdminApi(CreateAPIView):
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

        if channel.sum_admin_percents + percent > 90:
            raise InvalidPercentError()

        try:
            print("ok")
            ChannelAdmin.objects.create(channel=channel, admin=admin, percent=percent)
            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            raise InvalidChannelIdError()


class GetChannelAdministrationDataApi(RetrieveAPIView):

    def retrieve(self, request, channel_id, *args, **kwargs):
        try:
            channel = Channel.objects.get(id=channel_id)
        except Exception as e:
            raise InvalidChannelIdError()

        subscriptions = Subscription.objects.filter(channel=channel)
        subscriptions_data = SubscriptionSerializer(subscriptions, many=True).data

        admins = ChannelAdmin.objects.filter(channel=channel)
        admins_data = AdminSerializer(admins, many=True).data

        members = Membership.objects.filter(channel=channel)
        members_data = MemberUserSerializer(members, many=True).data

        return Response({"subscriptions": subscriptions_data, "admins": admins_data, "members": members_data})


class ChannelAdminClearAccountApi(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous or (not user.admin_channels.all() and not user.owner_channels.all()):
            raise UnauthorizedError()

        if user.credit == 0:
            raise EmptyBalanceError()

        if not user.cc_number:
            raise IncompleteProfileError()

        if BankHelper().deposit_to_account(user.credit, user.cc_number):
            user.credit = 0
            user.save()
            return Response(status=status.HTTP_200_OK)


class AddContentApi(CreateAPIView):
    def create(self, request, channel_id, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            raise UnauthorizedError()

        try:
            channel = Channel.objects.get(id=channel_id)
        except Exception as e:
            raise InvalidChannelIdError()

        user_owner_channels = user.owner_channels.all().values_list("id", flat=True)
        user_admin_channels = user.admin_channels.all().values_list("channel_id", flat=True)

        if not channel_id in user_owner_channels and not channel_id in user_admin_channels:
            raise UnauthorizedError()

        try:
            type = request.data["type"]
            price = int(request.data["price"])
            summary = request.data["summary"]

        except:
            raise InvalidRequestError()

        content = Content.objects.create(
            type=type,
            price=price,
            summary=summary,
            sender=request.user,
            channel=channel,
            free=price == 0,
        )

        return Response(ChannelContentSerializer(content).data, status=status.HTTP_201_CREATED)


class AddContentFileApi(CreateAPIView):
    def create(self, request, content_id, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            raise UnauthorizedError()

        try:
            content = Content.objects.get(id=content_id)
        except Exception as e:
            raise InvalidContentIdError()

        if content.sender != request.user:
            raise UnauthorizedError()

        if content.type == ContentType.text:
            try:
                text = request.data["text"]
                content.text = text
                content.save()
                return Response(
                    # {"url": request.build_absolute_uri(user.avatar.url)},
                    status=status.HTTP_200_OK,
                )
            except:
                InvalidRequestError()

        attachment = request.FILES["attachment"]
        file_name, file_extension = os.path.splitext(attachment.name)

        if attachment.size > 10000000:
            raise InvalidRequestError()

        attachment.name = escape(attachment.name)

        if content.type == ContentType.image:
            if file_extension not in [".jpg", ".jpeg", ".svg", ".png", ".webp"]:
                raise InvalidRequestError()
            content.image = attachment
        elif content.type == ContentType.voice:
            if file_extension not in [".mp3", ".wav"]:
                raise InvalidRequestError()
            content.voice = attachment
        elif content.type == ContentType.video:
            if file_extension not in [".mp4", ".mkv"]:
                raise InvalidRequestError()
            content.video = attachment

        content.save()
        return Response(
            # {"url": request.build_absolute_uri(user.avatar.url)},
            status=status.HTTP_200_OK,
        )
