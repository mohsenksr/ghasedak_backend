from rest_framework.generics import CreateAPIView, RetrieveAPIView

from rest_framework.response import Response
from rest_framework import status
from apps.account.models import User
from apps.channel.exceptions import InvalidChannelIdError
from apps.channel.models import Channel, Subscription, Membership
from apps.channel.serializers import SubscriptionSerializer, MemberUserSerializer
from apps.channel_administration.exceptions import InvalidAdminIdError, InvalidPercentError, EmptyBalanceError, \
    IncompleteProfileError
from apps.channel_administration.models import ChannelAdmin
from apps.channel_administration.serializers import AdminSerializer
from apps.shared import UnauthorizedError, InvalidRequestError
from utils.helpers.bank_helper import BankHelper


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

        if channel.sum_admin_percents + percent > 100:
            raise InvalidPercentError()

        try:
            print("ok")
            ChannelAdmin.objects.create(channel=channel, admin=admin, percent=percent)
            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            raise InvalidChannelIdError()


class GetChannelAdministrationApi(RetrieveAPIView):

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
