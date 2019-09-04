import unittest
import jwt
import time
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

    @mock.patch('sparrow_cloud.utils.get_settings_value.GetSettingsValue.get_middleware_value', return_value='123131313')
    @mock.patch('rest_framework.authentication.get_authorization_header', return_value=AUTH)
    def test_users(self, get_authorization_header, get_middleware_value):
        from sparrow_cloud.middleware.jwt_middleware import JWTMiddleware
        self.assertEqual(JWTMiddleware().process_request(MockRequest()), None)


if __name__ == '__main__':
    unittest.main()
