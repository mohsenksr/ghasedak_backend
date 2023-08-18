from rest_framework.test import APITestCase


class NotEqualObjectsException(Exception):
    pass


class BaseAPITestCase(APITestCase):
    def assertObjectKeysEqual(self, obj1, obj2):
        for k1 in obj1.keys():
            if k1 not in obj2.keys():
                raise NotEqualObjectsException()
            if isinstance(obj1[k1], dict):
                self.assertObjectKeysEqual(obj1[k1], obj2[k1])
        if set(obj1.keys()) != set(obj2.keys()):
            raise NotEqualObjectsException()
