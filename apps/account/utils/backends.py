from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from apps.account.exceptions import UserNotFoundError
from utils.general.cache_handler import check_in_cache

User = get_user_model()


class PhoneBackend(BaseBackend):
    def authenticate(self, request, phone=None, code=None, **kwargs):
        if check_in_cache(phone, code):
            try:
                return User.objects.get(phone=phone)
            except User.DoesNotExist:
                raise UserNotFoundError()
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
