from apps.channel.apis import GetUserChannelsApi, CreateChannelApi, JoinChannelApi, GetChannelDescriptionApi, \
    GetChannelContentsApi, CreateSubscriptionApi
from django.urls import path, include

urlpatterns = [
    path('', GetUserChannelsApi.as_view(), name='get-channels'),
    path('create/', CreateChannelApi.as_view(), name='create-channel'),
    path('join/<str:channel_id>/', JoinChannelApi.as_view(), name='join-channel'),
    path('contents/<str:channel_id>/', GetChannelContentsApi.as_view(), name='join-channel'),
    path('description/<str:channel_id>/', GetChannelDescriptionApi.as_view(), name='channel-description'),
    path('subscription/create/', CreateSubscriptionApi.as_view(), name='create-subscription'),
]



