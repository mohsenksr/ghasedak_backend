from rest_framework import serializers

from apps.account.models import User, UserRoles
from apps.shared.serializers.read_only_model_serializer import ReadOnlyModelSerializer


class UserLeanSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name']


class UserInfoSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name',
                  'first_name', 'last_name',
                  'phone', 'email', 'credit']


class UserSetProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'national_id', 'cc_number']
