from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import gettext as _

from ghasedak.storage_backends import MediaStorage

post_image_storage = MediaStorage(location=f'{MediaStorage.BASE_LOCATION}/posts/image')
post_voice_storage = MediaStorage(location=f'{MediaStorage.BASE_LOCATION}/posts/voice')
post_video_storage = MediaStorage(location=f'{MediaStorage.BASE_LOCATION}/posts/video')


class Channel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)
    creator = models.ForeignKey(
        to="account.User",
        related_name="owner_channels",
        on_delete=models.CASCADE, null=False,
        blank=False,
    )
    archived = models.BooleanField(default=False)
    title = models.CharField(max_length=64, null=False, blank=False)
    channel_id = models.CharField(max_length=32, null=False, blank=False, unique=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.channel_id

    @property
    def sum_admin_percents(self):
        sum = 0
        for admin in self.admins.all():
            sum += admin.percent
        return sum


class Membership(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    channel = models.ForeignKey(to=Channel, related_name="members", on_delete=models.CASCADE)
    user = models.ForeignKey(to="account.User", related_name="member_channels", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "channel",)

    def __str__(self):
        return self.user.username + " - " + self.channel.title


class SubscriptionDuration(models.TextChoices):
    one_month = "1month", _("1month")
    three_months = "3months", _("3months")
    six_months = "6months", _("6months")
    twelve_months = "12months", _("12months")


class Subscription(models.Model):
    price = models.IntegerField(null=False, blank=False)
    channel = models.ForeignKey(to=Channel, related_name="subscriptions", on_delete=models.CASCADE)
    duration = models.CharField(
        max_length=16,
        choices=SubscriptionDuration.choices,
        default=SubscriptionDuration.one_month,
        null=False,
        blank=False,
    )

    class Meta:
        unique_together = ("duration", "channel",)

    def __str__(self):
        return self.channel.title + " - " + self.duration


class UserSubscription(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    subscription = models.ForeignKey(to=Subscription, related_name="users", on_delete=models.CASCADE)
    user = models.ForeignKey(to="account.User", related_name="subscriptions", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "subscription",)

    def __str__(self):
        return str(self.subscription) + " - " + self.user.username

    @property
    def is_active(self):
        active = True
        if self.subscription.duration == SubscriptionDuration.one_month:
            active = datetime.now().date() - self.created_date.date() < timedelta(days=30)
        elif self.subscription.duration == SubscriptionDuration.three_months:
            active = datetime.now().date() - self.created_date.date() < timedelta(days=90)
        elif self.subscription.duration == SubscriptionDuration.six_months:
            active = datetime.now().date() - self.created_date.date() < timedelta(days=180)
        elif self.subscription.duration == SubscriptionDuration.twelve_months:
            active = datetime.now().date() - self.created_date.date() < timedelta(days=360)

        if not active:
            self.delete()
            return False

        return True


class ContentType(models.TextChoices):
    text = "text", _("text")
    voice = "voice", _("voice")
    image = "image", _("image")
    video = "video", _("video")


class Content(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    channel = models.ForeignKey(to=Channel, related_name="posts", on_delete=models.CASCADE)
    sender = models.ForeignKey(to="account.User", related_name="posts", on_delete=models.CASCADE)
    type = models.CharField(max_length=16, choices=ContentType.choices, default=ContentType.text)
    price = models.IntegerField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(storage=post_image_storage, null=True, blank=True)
    video = models.FileField(storage=post_video_storage, null=True, blank=True)
    voice = models.FileField(storage=post_voice_storage, null=True, blank=True)
    edited = models.BooleanField(default=False)
    free = models.BooleanField(default=False)

    def __str__(self):
        return str(self.channel) + " - " + str(self.created_date)


class UserBoughtContent(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    content = models.ForeignKey(to=Content, related_name="users", on_delete=models.CASCADE)
    user = models.ForeignKey(to="account.User", related_name="payed_contents", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "content",)

    def __str__(self):
        return str(self.content) + " - " + self.user.username
