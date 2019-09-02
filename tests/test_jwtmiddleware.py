import unittest
from unittest import mock

from sparrow_cloud.auth.user import User


AUTH = b'Token eyJhUzI1NiIs'
USER_ID = '3aa60781234547a5b94a095588999999'
PAYLOAD = {'uid': '3aa60781234547a5b94a095588999999', 'app_id': 'app_0000',
           'exp': 0000, 'iat': 1111, 'iss': 'd'}
USER = User(user_id=USER_ID)


class MockRequest(object):
    META = {}


class TestJWTAuthentication(unittest.TestCase):

    @mock.patch('rest_framework.authentication.get_authorization_header', return_value=AUTH)
    @mock.patch('sparrow_cloud.utils.get_settings_value', return_value='sparrow_cloud.auth.user.User')
    @mock.patch('django.conf.settings', return_value='')
    @mock.patch('sparrow_cloud.utils.decode_jwt.DecodeJwt.decode_jwt', return_value=PAYLOAD)
    @mock.patch('sparrow_cloud.utils.get_settings_value.GetSettingsValue.get_middleware_value',
                return_value='mock_value')
    def test_users(self, get_middleware_value, DecodeJwt, settings, get_settings_value,
                 get_authorization_header):
        from sparrow_cloud.middleware.jwt_middleware import JWTMiddleware
        self.assertEqual(JWTMiddleware().process_request(MockRequest()), None)


if __name__ == '__main__':
    unittest.main()