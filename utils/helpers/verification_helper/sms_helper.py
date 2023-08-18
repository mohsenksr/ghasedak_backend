from kavenegar import *
import json
from decouple import config

from utils.helpers.verification_helper.verification_helper import VerificationHelper


class SMSVerificationHelper(VerificationHelper):
    def send_verification_code(self, phone, code):
        try:
            return True
            # api = KavenegarAPI(config('KAVEHNEGAR_API_KEY'))
            # response = api.verify_lookup(params={"receptor": phone, "token": code, "template": config("KAVEHNEGAR_TEMPLATE_NAME")})
            # if response[0]["status"] == 5:
            #     return True
            # else:
            #     return False
        except APIException as e:
            return False
        except HTTPException as e:
            return False
