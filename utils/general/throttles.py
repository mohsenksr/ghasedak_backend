from rest_framework.throttling import UserRateThrottle


class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
