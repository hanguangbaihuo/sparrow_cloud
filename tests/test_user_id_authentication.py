import unittest
import importlib
import os
from django.conf import settings
from unittest import mock

from sparrow_cloud.auth.user import User


AUTH = b'Token eyJhUzI1NiIs'
USER_ID = '3aa60781234547a5b94a095588999999'
PAYLOAD = {'uid': '3aa60781234547a5b94a095588999999', 'app_id': 'app_0000',
           'exp': 0000, 'iat': 1111, 'iss': 'd'}
USER = User(user_id=USER_ID)


class MockRequest(object):
    META = {
        "payload": PAYLOAD,
        "REMOTE_USER": USER_ID
    }


def value():
    user_class_path = "sparrow_cloud.auth.user.User"
    module_path, cls_name = user_class_path.rsplit(".", 1)
    user_cls = getattr(importlib.import_module(module_path), cls_name)
    user = user_cls(user_id=USER_ID)
    return user


class TestUserIDAuthentication(unittest.TestCase):
    """测试 UserIDAuthentication"""

    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
        settings.SPARROW_AUTHENTICATION = {"USER_CLASS_PATH": "sparrow_cloud.auth.user.User"}

    def test_user(self):
        from sparrow_cloud.auth.user_id_authentication import UserIDAuthentication
        user_info = UserIDAuthentication().authenticate(MockRequest())
        user = user_info[0]
        payload = user_info[1]
        _user = value()
        self.assertEqual(type(user), type(_user))
        self.assertEqual(payload, PAYLOAD)

    def tearDown(self):
        del os.environ["DJANGO_SETTINGS_MODULE"]


if __name__ == '__main__':
    unittest.main()