import os
import unittest
import django
from sparrow_cloud.utils.get_hash_key import get_hash_key


class TestGetAppToken(unittest.TestCase):

    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
        from django.conf import settings
        self.setup_settings(settings)
        django.setup()

    def test_app_hash_key(self):
        app_token = get_hash_key(key_type="app")
        self.assertEqual(app_token, "APP_TOKEN_B9B9023")

    def test_user_hash_key(self):
        user_token = get_hash_key(key_type="user", user_id="21424kvjbcdjslafds")
        self.assertEqual(user_token, "USER_TOKEN_4238378")

    def setup_settings(self, settings):
        settings.SERVICE_CONF = {
            "NAME": "sparrow_cloud",
            "SECRET": "124cdsalhdisahgisabjnjlk"
        }