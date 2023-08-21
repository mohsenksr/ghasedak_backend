from django.urls import path, include

from apps.channel_administration.apis import CreateAdminApi

urlpatterns = [
    path('create/', CreateAdminApi.as_view(), name='create-admin'),
]



