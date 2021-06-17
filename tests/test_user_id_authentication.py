
import base64
from django.conf import settings
# import importlib
import json
import os
import unittest
# from unittest import mock

PAYLOAD = {'uid': '1234abc', 'app_id': 'core',
           'exp': 1722200316, 'iat': 1622193116, 'iss': 'test'}

# class MockDjangoSetting(object):
#     SPARROW_AUTHENTICATION = {"USER_CLASS_PATH": "sparrow_cloud.auth.user.User"}

class MockEmptyRequest(object):
    META = {}

class MockB64Request(object):
    META = {
        "X-Jwt-Payload": base64.b64encode(json.dumps(PAYLOAD).encode('utf-8')).decode('utf-8')
    }

class MockTextRequest(object):
    META = {
        "X-Jwt-Payload": json.dumps(PAYLOAD)
    }

class TestUserIDAuthentication(unittest.TestCase):
    """测试 UserIDAuthentication"""

    def setUp(self):
        # 配置Django的settings环境变量为当前目录中的mock_settings.py文件
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
        # 配置django的settings环境变量中的SPARROW_AUTHENTICATION
        settings.SPARROW_AUTHENTICATION = {"USER_CLASS_PATH": "sparrow_cloud.auth.user.User"}

    def test_empty_user(self):
        '''
        测试 空request.META
        '''
        from sparrow_cloud.auth.user_id_authentication import UserIDAuthentication
        res = UserIDAuthentication().authenticate(MockEmptyRequest())
        self.assertIsNone(res)

    def test_base64_type_user(self):
        '''
        测试 base64编码格式X-Jwt-Payload的request.META
        '''
        from sparrow_cloud.auth.user_id_authentication import UserIDAuthentication
        res = UserIDAuthentication().authenticate(MockB64Request())
        self.assertIsNotNone(res)
        self.assertIsInstance(res, tuple)
        self.assertEqual(len(res), 2)
        user, auth = res
        self.assertEqual(auth, PAYLOAD)
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.payload)

    def test_text_type_user(self):
        '''
        测试 文本编码格式X-Jwt-Payload的request.META
        '''
        from sparrow_cloud.auth.user_id_authentication import UserIDAuthentication
        res = UserIDAuthentication().authenticate(MockTextRequest())
        self.assertIsNotNone(res)
        self.assertIsInstance(res, tuple)
        self.assertEqual(len(res), 2)
        user, auth = res
        self.assertEqual(auth, PAYLOAD)
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.payload)

    def tearDown(self):
        del os.environ["DJANGO_SETTINGS_MODULE"]

if __name__ == '__main__':
    unittest.main()