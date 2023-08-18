from logging import getLogger
from decouple import config
import requests
import json
from rest_framework.response import Response
from rest_framework import status

from utils.exceptions import FailedDependency
from utils.general.logger import Logger

logger = getLogger()


class ZarinPalHelper:
    def send_start_request(self, amount, callback_url, description):
        MERCHANT = config("ZARINPAL_MERCHANT")
        payment_url = config("ZARINPAL_URL")
        start_payment_url = config("ZARINPAL_START_PAYMENT_URL")

        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "callback_url": callback_url,
            "description": description,
        }
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req = requests.post(url=payment_url, data=json.dumps(
            req_data), headers=req_header)
        print(req.json())
        Logger().error(logger, req.json())

        if len(req.json()['errors']) == 0:
            authority = req.json()['data']['authority']
            return Response({"link": start_payment_url.format(authority=authority)}, status=status.HTTP_200_OK)
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            raise FailedDependency()

    def verify_request(self, request, amount):
        MERCHANT = config("ZARINPAL_MERCHANT")
        verify_payment_url = config("ZARINPAL_VERIFY_URL")

        transaction_status = request.GET.get('Status')
        if transaction_status == 'OK':
            t_authority = request.GET['Authority']
            req_header = {"accept": "application/json",
                          "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": amount,
                "authority": t_authority
            }
            req = requests.post(url=verify_payment_url, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    return True, "reference_id: " + str(req.json()['data']['ref_id'])
                elif t_status == 101:
                    return True, None
                else:
                    return False, "error: " + req.json()['data']['message']
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return False, f"Error code: {e_code}, Error Message: {e_message}"
        else:
            return False, "error: " + "Transaction failed or canceled by user"
