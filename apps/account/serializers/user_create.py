from rest_framework import serializers

from apps.account.exceptions import InvalidTokenError
from apps.account.models import User, validate_user_role
from ghasedak.constants import SIGN_UP_TOKEN_PREFIX
from utils.general.cache_handler import check_in_cache


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, style={'input_type': 'password'}, write_only=True)
    role = serializers.CharField(validators=[validate_user_role])
    token = serializers.CharField()

    class Meta:
        model = User
        fields = ['token', 'email', 'first_name', 'last_name', 'password', 'role']

    def validate_token(self, value):
        if not check_in_cache(SIGN_UP_TOKEN_PREFIX + value.split("::")[1], value):
            raise InvalidTokenError()
        return value

    def create(self, validated_data):
        first_name, last_name = validated_data['first_name'], validated_data['last_name']
        phone, email = validated_data['token'].split('::')[1], validated_data['email']
        role, password = validated_data['role'], validated_data['password']
        user = User.objects.create_user(
            username=phone,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            role=role
        )
        return user
