import django
import unittest
from unittest import mock
from sparrow_cloud.authorization.token import *


MOCK_RESPONSE = {
    "expires_in": 7200,
    "token": "eyJhbGciOiJIUzI1.eyJ1aWQiOcCJ9.cayn"
}


class TestGetAppToken(unittest.TestCase):

    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
        from django.conf import settings
        self.setup_settings(settings)
        django.setup()

    @mock.patch('sparrow_cloud.restclient.rest_client.post', return_value=MOCK_RESPONSE)
    def test_get_user_token(self, mock_post):
        user_token = get_user_token(user_id="21424kvjbcdjslafds")
        self.assertEqual(user_token, MOCK_RESPONSE)

    @mock.patch('sparrow_cloud.restclient.rest_client.post', return_value=MOCK_RESPONSE)
    def test_get_app_token(self, mock_post):
        app_token = get_app_token()
        self.assertEqual(app_token, MOCK_RESPONSE)

    def setup_settings(self, settings):
        settings.SERVICE_CONF = {
            "NAME": "sparrow_cloud",
            "SECRET": "124cdsalhdisahgisabjnjlk"
        }