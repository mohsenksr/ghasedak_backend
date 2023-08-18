from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField
from rest_framework_simplejwt.settings import api_settings
from rest_framework import exceptions

from apps.account.models import LoginTypes


class TokenObtainSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        login_type = None
        if 'login_type' in kwargs:
            login_type = kwargs.pop('login_type')
        super().__init__(*args, **kwargs)
        if login_type:
            if login_type is LoginTypes.PHONE:
                self.fields.pop(self.username_field)
                self.fields.pop('password')
                self.fields['phone'] = serializers.CharField()
                self.fields['code'] = serializers.CharField()
                self.login_type = LoginTypes.PHONE
                return
        self.login_type = LoginTypes.PASSWORD
        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        if self.login_type is LoginTypes.PHONE:
            authenticate_kwargs = {
                'phone': attrs['phone'],
                'code': attrs['code']
            }
        else:
            authenticate_kwargs = {
                self.username_field: attrs[self.username_field],
                'password': attrs['password'],
            }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
        data = {}
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['name'] = user.full_name
        return token
