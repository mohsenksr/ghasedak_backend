from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # if isinstance(exc, ValidationError):
        #     exc.default_code = "invalid_input"
        #     exc.default_detail = _("Some field is required.")
        response.data = _handel_generic_error(exc)
    return response


def _handel_generic_error(exc):
    try:
        version = exc.version
    except:
        version = 'v1'
    return {
        'error': {
            'code': exc.default_code,
            'detail': exc.default_detail,
            'version': version
        }
    }
