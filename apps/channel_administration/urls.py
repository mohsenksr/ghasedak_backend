from django.urls import path, include

from apps.channel_administration.apis import CreateAdminApi, ChannelAdminClearAccountApi, \
    GetChannelAdministrationDataApi, AddContentApi, AddContentFileApi

urlpatterns = [
    path('data/<str:channel_id>/', GetChannelAdministrationDataApi.as_view(), name='channel-admin'),
    path('create/', CreateAdminApi.as_view(), name='create-admin'),
    path('clear/', ChannelAdminClearAccountApi.as_view(), name='clear-account'),
    path('content/add/<str:channel_id>/', AddContentApi.as_view(), name='add-content'),
    path('content/add-file/<str:content_id>/', AddContentFileApi.as_view(), name='add-content'),
]
