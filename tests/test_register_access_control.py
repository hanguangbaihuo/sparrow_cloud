import unittest
from unittest import mock
import django
from io import StringIO
from django.core.management import call_command
from django.conf.urls import url
from django.http import HttpResponse
import os


urlpatterns = []


class RestClientTestCase(unittest.TestCase):

    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
        from django.conf import settings
        self.setup_settings(settings)
        django.setup()

        from rest_framework.decorators import api_view

        @api_view()
        def detail(request):
            return HttpResponse("ok")

        urlpatterns.extend([
                    url(r'^/register/$', detail),
                    ]
                )

    @mock.patch('sparrow_cloud.restclient.rest_client.post', return_value={})
    def test_register_access_control(self, mock_post):
        out = StringIO()
        os.environ["SPARROW_ACCESS_CONTROL"] = "127.0.0.1:8001"
        call_command('register_access_control', stdout=out)
        r = out.read()
        print(r)
        self.assertEqual(r, '')

    def tearDown(self):
        del os.environ["SPARROW_ACCESS_CONTROL"]

    def setup_settings(self, settings):
        settings.XX = "1"
        settings.SECRET_KEY = "ss"
        settings.ROOT_URLCONF = __name__
        settings.CONSUL_CLIENT_ADDR = {
            "HOST": os.environ.get("CONSUL_IP", "127.0.0.1"),  # 在k8s上的环境变量类型：变量/变量引用
            "PORT": os.environ.get("CONSUL_PORT", 8500)
        }
        settings.ACCESS_CONTROL = {
            "ACCESS_CONTROL_SERVICE": {
                "ENV_NAME": "SPARROW_ACCESS_CONTROL",
                "VALUE": os.environ.get("SPARROW_ACCESS_CONTROL", "sparrow_access_control"),
            },
            "VERIFY_API_PATH": "/verify/",
            "REGISTER_API_PATH": "/register/",
            "ACCESS_CONTROL_CLASS": "sparrow_cloud.apps.access_control.example_access_control.ExampleAccessControl",
            "SECRET": "fdsafgxckrewkrjfvlxosdg"
        }
        settings.SERVICE_CONF = {
            "NAME": "test"
        }


