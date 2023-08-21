from rest_framework import serializers

from apps.channel_administration.models import ChannelAdmin


class CreateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelAdmin
        fields = ("admin", "channel", "percent",)
