import django
import json
import unittest
from unittest import mock
from django.core.cache import cache
from sparrow_cloud.authorization.token import *
from sparrow_cloud.utils.get_hash_key import get_hash_key

MOCK_USER_RESPONSE = {
    "iss": "sparrow_app_manage",
    "exp": 1622800021,
    "iat": 1622792821,
    "uid": "test_user_id_succ_abc123",
    "type": "user"
}
MOCK_APP_RESPONSE = {
    "iss": "sparrow_app_manage",
    "exp": 1622800182,
    "iat": 1622792982,
    "uid": "sparrow_cloud",
    "type": "app"
}

class UserGoodResp:
    status_code = 200
    text = json.dumps(MOCK_USER_RESPONSE)

class BadResp:
    status_code = 400
    text = '{"message":"bad request"}'

class AppGoodResp:
    status_code = 200
    text = json.dumps(MOCK_APP_RESPONSE)

class TestGetUserToken(unittest.TestCase):

    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
        from django.conf import settings
        self.setup_settings(settings)
        django.setup()

    def setup_settings(self, settings):
        settings.SERVICE_CONF = {
            "NAME": "sparrow_cloud",
            "SECRET": "124cdsalhdisahgisabjnjlk"
        }

    @mock.patch('sparrow_cloud.restclient.requests_client.post', return_value=UserGoodResp)
    def test_get_user_token_succ(self, mock_post):
        token = get_user_token(user_id="test_user_id_succ_abc123")
        data = json.loads(token)
        self.assertIn("uid", data)
        self.assertEqual(data["uid"], MOCK_USER_RESPONSE["uid"])

    @mock.patch('sparrow_cloud.restclient.requests_client.post', return_value=BadResp)
    def test_get_user_token_fail(self, mock_post):
        token = get_user_token(user_id="fail_user_id_abc123")
        data = json.loads(token)
        # data为返回的静态数据，没有iat和exp键
        self.assertIn("uid", data)
        self.assertNotIn("exp", data)
        self.assertNotIn("iat", data)
    
    @mock.patch('sparrow_cloud.restclient.requests_client.post', return_value=UserGoodResp)
    def test_get_user_token_cache(self, mock_post):
        uid="test_cache_user_id"
        token = get_user_token(user_id=uid)
        data = json.loads(token)
        self.assertIn("uid", data)
        # 测试一次请求之后，检查缓存中是否已经缓存该token，并且缓存中与函数返回的数据相同
        user_token_key = get_hash_key(key_type="user", user_id=uid)
        cache_user_token = cache.get(user_token_key)
        self.assertEqual(token, cache_user_token)


class TestGetAppToken(unittest.TestCase):
    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
        from django.conf import settings
        self.setup_settings(settings)
        django.setup()

    def setup_settings(self, settings):
        settings.SERVICE_CONF = {
            "NAME": "sparrow_cloud",
            "SECRET": "124cdsalhdisahgisabjnjlk"
        }

    @mock.patch('sparrow_cloud.restclient.requests_client.post', return_value=AppGoodResp)
    def test_get_app_token_succ(self, mock_post):
        app_token = get_app_token()
        data = json.loads(app_token)
        self.assertIn("uid", data)
        self.assertEqual(data["uid"], MOCK_APP_RESPONSE["uid"])

    @mock.patch('sparrow_cloud.restclient.requests_client.post', return_value=BadResp)
    def test_get_app_token_fail(self, mock_post):
        token = get_app_token()
        data = json.loads(token)
        # data为返回的静态数据，没有iat和exp键
        self.assertIn("uid", data)
        self.assertNotIn("exp", data)
        self.assertNotIn("iat", data)
    
    @mock.patch('sparrow_cloud.restclient.requests_client.post', return_value=AppGoodResp)
    def test_get_app_token_cache(self, mock_post):
        app_token = get_app_token()
        data = json.loads(app_token)
        self.assertIn("uid", data)
        # 测试一次请求之后，检查缓存中是否已经缓存该token，并且缓存中与函数返回的数据相同
        app_token_key = get_hash_key(key_type="app")
        cache_app_token = cache.get(app_token_key)
        self.assertEqual(app_token, cache_app_token)
    
    def tearDown(self):
        app_token_key = get_hash_key(key_type="app")
        cache.delete(app_token_key)