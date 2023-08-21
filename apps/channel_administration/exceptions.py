from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class InvalidAdminIdError(APIException):
    status_code = 400
    default_detail = _('incorrect admin id')
    default_code = 'incorrect admin id'


class InvalidPercentError(APIException):
    status_code = 400
    default_detail = _('incorrect percent')
    default_code = 'incorrect percent'
