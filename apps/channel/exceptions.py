from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class InvalidChannelIdError(APIException):
    status_code = 400
    default_detail = _('incorrect channel id')
    default_code = 'incorrect channel id'


class InvalidSubscriptionIdError(APIException):
    status_code = 400
    default_detail = _('incorrect subscription id')
    default_code = 'incorrect subscription id'


class AlreadyBoughtError(APIException):
    status_code = 400
    default_detail = _('already bought')
    default_code = 'already bought'
