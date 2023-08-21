from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class UserNotFoundError(APIException):
    status_code = 404

    def __init__(self, detail=_('user was not found with this username')):
        self.default_code = 'user_not_found_error'
        super().__init__(detail, self.default_code)
        self.default_detail = detail


class IncorrectPasswordError(APIException):

    def __init__(self, detail=_('incorrect password for this user was provided')):
        self.default_code = 'incorrect_password_error'
        super().__init__(detail, self.default_code)
        self.default_detail = detail


class IncorrectPhoneError(APIException):
    status_code = 400

    def __init__(self, detail=_('incorrect phone number')):
        self.default_code = 'incorrect_phone_error'
        super().__init__(detail, self.default_code)
        self.default_detail = detail


class InvalidTokenError(APIException):
    status_code = 400

    def __init__(self, detail=_('invalid token')):
        self.default_code = 'invalid_token_error'
        super().__init__(detail, self.default_code)
        self.default_detail = detail


class InvalidFieldsError(APIException):
    status_code = 400

    def __init__(self, detail=_('invalid fields error')):
        self.default_code = 'invalid_fields_error'
        super().__init__(detail, self.default_code)
        self.default_detail = detail


class AddressNotFoundError(APIException):
    status_code = 404
    default_detail = _('address not found')
    default_code = 'address_not_found'


class NationalIdRequiredError(APIException):
    status_code = 400
    default_detail = _('national id required')
    default_code = 'national_id_required'
