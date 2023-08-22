from rest_framework import serializers

from apps.channel_administration.models import ChannelAdmin


class AdminSerializer(serializers.ModelSerializer):
    admin = serializers.CharField(source="admin.full_name")

    class Meta:
        model = ChannelAdmin
        fields = ("id", "admin", "channel", "percent",)
