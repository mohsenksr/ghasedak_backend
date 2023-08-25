from rest_framework import serializers

from apps.channel.models import Channel, Content, Membership, Subscription
from apps.channel_administration.models import ChannelAdmin


class ChannelLeanSerializer(serializers.ModelSerializer):
    last_content = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ["id", "title", "last_content"]

    def get_last_content(self, channel: Channel):
        if channel.posts.all():
            return channel.posts.last().created_date
        else:
            return channel.created_date


class AdminChannelLeanSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="channel.id")
    title = serializers.CharField(source="channel.title")
    last_content = serializers.SerializerMethodField()

    class Meta:
        model = ChannelAdmin
        fields = ["id", "title", "last_content"]

    def get_last_content(self, admin_channel: ChannelAdmin):
        if admin_channel.channel.posts.all():
            return admin_channel.channel.posts.last().created_date
        else:
            return admin_channel.channel.created_date


class MemberChannelLeanSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="channel.id")
    title = serializers.CharField(source="channel.title")
    last_content = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = ["id", "title", "last_content"]

    def get_last_content(self, member_channel: Membership):
        if member_channel.channel.posts.all():
            return member_channel.channel.posts.last().created_date
        else:
            return member_channel.channel.created_date


class MemberUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    full_name = serializers.CharField(source="user.full_name")

    class Meta:
        model = Membership
        fields = ["created_date", "username", "full_name"]


class ChannelInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ["id", "channel_id", "title", "bio"]


class ChannelContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ["id", "created_date", "type", "free", "summary", "edited", "price"]


class ChannelContentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ["image", "video", "voice"]

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["id", "channel_id", "duration", "price"]
