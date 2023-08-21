from apps.shared import BankErrorOccurred
from utils.general.singleton import Singleton


class BankHelper(Singleton):
    def deposit_to_account(self, amount, cc_number):
        return True
        # raise BankErrorOccurred()

    def payment(self, amount):
        return True
        # raise BankErrorOccurred()

    def check_national_id(self, national_id, cc_number):
        return True
        # raise BankErrorOccurred()