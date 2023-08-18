from kavenegar import *

from utils.helpers.verification_helper.verification_helper import VerificationHelper


class EmailVerificationHelper(VerificationHelper):
    def send_verification_code(self, email, code):
        try:
            return True
        except APIException as e:
            return False
        except HTTPException as e:
            return False
