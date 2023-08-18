from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class IncompleteRequestError(APIException):
    status_code = 400
    default_detail = _('incomplete request')
    default_code = 'incomplete_request'


class InvalidRequestError(APIException):
    status_code = 400
    default_detail = _('invalid request')
    default_code = 'invalid_request'


class PageNotFoundError(APIException):
    status_code = 404
    default_detail = _('page not found')
    default_code = 'page_not_found'


class UnknownErrorOccurred(APIException):
    status_code = 400
    default_detail = _('unknown error occurred')
    default_code = 'unknown_error_occurred'
