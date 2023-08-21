from django.urls import path, include

from apps.channel_administration.apis import CreateAdminApi, ChannelAdminClearAccountApi, GetChannelAdministrationApi

urlpatterns = [
    path('data/<str:channel_id>/', GetChannelAdministrationApi.as_view(), name='channel-admin'),
    path('create/', CreateAdminApi.as_view(), name='create-admin'),
    path('clear/', ChannelAdminClearAccountApi.as_view(), name='clear-account'),
]
