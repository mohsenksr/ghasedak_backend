import random
import re
from secrets import token_hex

from django.contrib.auth import logout, get_user_model
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.account.exceptions import IncorrectPhoneError, UserNotFoundError, InvalidFieldsError, InvalidTokenError
from apps.account.models import LoginTypes
from apps.account.serializers import TokenObtainSerializer, UserCreateSerializer, UserInfoSerializer
from apps.shared import UnknownErrorOccurred
from ghasedak.constants import SIGN_UP_TOKEN_EXPIRE_TIME, SIGN_UP_TOKEN_PREFIX, PHONE_REGEX_PATTERN, \
    FORGET_PASSWORD_TOKEN_PREFIX
from utils.general.cache_handler import put_in_cache, check_in_cache
from django.utils.translation import gettext as _

from utils.helpers.verification_helper.email_helper import EmailVerificationHelper
from utils.helpers.verification_helper.sms_helper import SMSVerificationHelper

User = get_user_model()


def generate_token(phone, token_type='signup'):
    token_configs = {
        'signup': {
            'prefix': SIGN_UP_TOKEN_PREFIX,
            'expire_time': SIGN_UP_TOKEN_EXPIRE_TIME,
            'key': 'signup_token'
        },
        'forget-password': {
            'prefix': FORGET_PASSWORD_TOKEN_PREFIX,
            'expire_time': SIGN_UP_TOKEN_EXPIRE_TIME,
            'key': 'forget_token'
        }
    }
    config = token_configs[token_type]
    token = f'{token_hex(16)}::{phone}'
    put_in_cache(config['prefix'] + phone, token, exp_time=config['expire_time'])
    return Response({config['key']: token}, status=status.HTTP_200_OK)


class SignInAPI(TokenObtainPairView):
    serializer_class = TokenObtainSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         login_type=LoginTypes.PHONE
                                         if 'verify-code' in request.stream.path
                                         else LoginTypes.PASSWORD)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except UserNotFoundError as _:
            return generate_token(request.data['phone'])
        if request.query_params.get('action') == 'forget-password':
            return generate_token(request.data['phone'], token_type='forget-password')
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class AuthenticationAPI(APIView):
    def get(self, request, phone, *args, **kwargs):
        if not re.match(PHONE_REGEX_PATTERN, phone):
            raise IncorrectPhoneError(_('wrong phone number'))
        return send_verification_message("SMS", phone)


    #TODO: complete email registration
    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_info = UserInfoSerializer(user, context={'request': request}).data
        return Response(user_info, status=status.HTTP_200_OK)


class EmailAuthenticationAPI(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data["email"]
        return send_verification_message("EMAIL", email)


class ForgetPasswordAPI(APIView):

    def validate(self):
        if any(it not in self.request.data for it in ['password', 'token']) or '::' not in self.request.data['token']:
            raise InvalidFieldsError()

    def post(self, request, *args, **kwargs):
        self.validate()
        phone = request.data['token'].split('::')[1]
        if not check_in_cache(FORGET_PASSWORD_TOKEN_PREFIX + phone, request.data['token']):
            raise InvalidTokenError()
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise UserNotFoundError()
        user.set_password(request.data['password'])
        user.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', ])
def sign_out(request):
    logout(request)
    return Response()


def send_verification_message(message_type, dest):
    # code = str(random.randint(1000, 9999))
    code = "1234"
    put_in_cache(dest, code, exp_time=120)
    if message_type == "EMAIL":
        if EmailVerificationHelper().send_verification_code(dest, code):
            return Response({"code": code}, status=status.HTTP_200_OK)
        else:
            raise UnknownErrorOccurred()
    else:
        if SMSVerificationHelper().send_verification_code(dest, code):
            return Response({"code": code}, status=status.HTTP_200_OK)
        else:
            raise UnknownErrorOccurred()
