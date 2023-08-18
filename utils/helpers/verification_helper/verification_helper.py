from abc import ABC, abstractmethod


class VerificationHelper(ABC):
    @abstractmethod
    def send_verification_code(self, dest, code):
        pass
