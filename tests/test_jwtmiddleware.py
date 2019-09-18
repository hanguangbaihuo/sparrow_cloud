import unittest
import jwt
import time
import os
from django.conf import settings
from unittest import mock

from sparrow_cloud.auth.user import User


USER_ID = '1112313123'
PAYLOAD = {"uid": "1112313123", "app_id": "app_0000",
           "exp": int(time.time()+60*60), "iat": int(time.time()), "iss": "backend"}
AUTH = b'Token '+jwt.encode(PAYLOAD, '123131313', algorithm='HS256')
USER = User(user_id=USER_ID)


class MockRequest(object):
    META = {}


class TestJWTAuthentication(unittest.TestCase):

    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
        settings.JWT_MIDDLEWARE = {
            "JWT_SECRET": "123131313",  # JWT_SECRET, 必填
        }

    @mock.patch('rest_framework.authentication.get_authorization_header', return_value=AUTH)
    def test_users(self, get_authorization_header):
        from sparrow_cloud.middleware.jwt_middleware import JWTMiddleware
        self.assertEqual(JWTMiddleware().process_request(MockRequest()), None)

    def tearDown(self):
        del os.environ["DJANGO_SETTINGS_MODULE"]


if __name__ == '__main__':
    unittest.main()
