from apps.channel.apis import GetUserChannelsApi, CreateChannelApi, JoinChannelApi, GetChannelDescriptionApi, \
    GetChannelContentsApi, CreateSubscriptionApi, GetChannelSubscriptionsApi, SellSubscriptionApi, SellContentApi, \
    GetChannelContentFileApi

from django.urls import path, include

urlpatterns = [
    path('', GetUserChannelsApi.as_view(), name='get-channels'),
    path('create/', CreateChannelApi.as_view(), name='create-channel'),
    path('join/<str:channel_id>/', JoinChannelApi.as_view(), name='join-channel'),
    path('content/get/<str:channel_id>/', GetChannelContentsApi.as_view(), name='channel-contents'),
    path('content/get-file/<str:content_id>/', GetChannelContentFileApi.as_view(), name='content-file'),
    path('content/sell/<str:content_id>/', SellContentApi.as_view(), name='sell-content'),
    path('description/<str:channel_id>/', GetChannelDescriptionApi.as_view(), name='channel-description'),
    path('subscription/get/<str:channel_id>/', GetChannelSubscriptionsApi.as_view(), name='get-subscriptions'),
    path('subscription/create/', CreateSubscriptionApi.as_view(), name='create-subscription'),
    path('subscription/sell/<str:subscription_id>/', SellSubscriptionApi.as_view(), name='sell-subscription'),
]
