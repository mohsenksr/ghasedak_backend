from django.contrib import admin

from apps.channel.models import Channel, Membership, Subscription, UserSubscription, Content


@admin.register(Channel)
class ChannelModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_date', 'creator', 'title', 'channel_id')
    search_fields = ('id', 'channel_id', 'creator', 'title')
    raw_id_fields = ('creator',)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'channel', 'user',)
    search_fields = ('id', 'channel',)
    raw_id_fields = ('channel', 'user',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'channel', 'price', 'duration')
    search_fields = ('id', 'channel',)
    raw_id_fields = ('channel',)


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'user', 'created_date')
    search_fields = ('id', 'subscription__id', 'subscription__channel__id', 'user__username')
    raw_id_fields = ('subscription', 'user',)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'channel', 'type', 'created_date')
    search_fields = ('id', 'channel__title', 'channel__id')
    raw_id_fields = ('channel', 'sender',)
