import os

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, DestroyAPIView
from django.utils.html import escape

from apps.account.exceptions import NationalIdRequiredError
from apps.account.models import User
from apps.account.serializers import UserSetProfileSerializer, UserInfoSerializer
from rest_framework import status

from apps.shared import InvalidRequestError
from utils.helpers.bank_helper import BankHelper


class ProfileApi(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        match self.action:
            case 'retrieve':
                return UserInfoSerializer
            case 'update':
                return UserSetProfileSerializer

    def get_object(self):
        return self.queryset.get(id=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        self.get_serializer_context().update({'request': request})
        data = self.get_serializer(instance=user).data
        return Response(data=data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        kwargs.update({'partial': True})
        if "cc_number" in request.data:
            if not "national_id" in request.data:
                raise NationalIdRequiredError()

        BankHelper().check_national_id(request.data["national_id"], request.data["cc_number"])
        
        return super().update(request, *args, **kwargs)


class ProfileAvatarApi(ModelViewSet):
    def create(self, request, *args, **kwargs):
        attachment = request.FILES["attachment"]
        file_name, file_extension = os.path.splitext(attachment.name)
        if attachment.content_type not in [
            "image/jpeg",
            "image/png",
            "image/svg+xml",
            "image/webp",
        ]:
            raise InvalidRequestError()

        if file_extension not in [".jpg", ".jpeg", ".svg", ".png", ".webp"]:
            raise InvalidRequestError()

        if attachment.size > 1000000:
            raise InvalidRequestError()

        attachment.name = escape(attachment.name)

        user = User.objects.get(id=request.user.id)
        user.avatar = attachment
        user.save()
        return Response(
            # {"url": request.build_absolute_uri(user.avatar.url)},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        user.avatar = None
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


profile_api = ProfileApi.as_view({
    'get': 'retrieve',
    'post': 'update',
})

profile_avatar_api = ProfileAvatarApi.as_view({
    'delete': 'destroy',
    'post': 'create',
})
