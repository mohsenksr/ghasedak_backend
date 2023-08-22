from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class InvalidChannelIdError(APIException):
    status_code = 400
    default_detail = _('incorrect channel id')
    default_code = 'incorrect channel id'


class InvalidContentIdError(APIException):
    status_code = 400
    default_detail = _('incorrect content id')
    default_code = 'incorrect content id'


class InvalidSubscriptionIdError(APIException):
    status_code = 400
    default_detail = _('incorrect subscription id')
    default_code = 'incorrect subscription id'


class AlreadyBoughtError(APIException):
    status_code = 400
    default_detail = _('already bought')
    default_code = 'already bought'


class InappropriateApiError(APIException):
    status_code = 400
    default_detail = _('inappropriate api')
    default_code = 'inappropriate api'
