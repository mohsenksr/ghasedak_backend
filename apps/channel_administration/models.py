from django.db import models


class ChannelAdmin(models.Model):
    admin = models.ForeignKey(
        to="account.User",
        related_name="admin_channels",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    channel = models.ForeignKey(to="channel.Channel", related_name="admins", on_delete=models.CASCADE)
    percent = models.IntegerField()

