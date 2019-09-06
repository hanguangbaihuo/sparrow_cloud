import unittest
from unittest import mock
import os
import django


from io import StringIO
from django.core.management import call_command
from django.test import TestCase

# class ClosepollTest(TestCase):
#     def test_command_output(self):
#         out = StringIO()
#         call_command('register_api_permission', stdout=out)
#         self.assertIn('Expected output', out.getvalue())


import os
from django.conf.urls import url
from django.http import HttpResponse


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


urlpatterns = [
    url(r'^/ssss/$', detail)
]



class RestClientTestCase(unittest.TestCase):

    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
        
    def test_get(self):
        from django.conf import settings
        # import pdb; pdb.set_trace()
        # 配置 settings, 初始化 settings
        # import pdb; pdb.set_trace()
        # settings.configure()
        #  初始化
        self.setup_settings(settings)
        
        django.setup()
        # import pdb; pdb.set_trace()
        out = StringIO()
        # call_command('rap', stdout=out)
        # import pdb; pdb.set_trace()
        call_command('register_api_permission', '-d', '2', stdout=out)
        
        print(settings)


    def setup_settings(self, settings):
        settings.XX = "1"
        settings.SECRET_KEY = "ss"
        settings.INSTALLED_APPS = [
            "sparrow_cloud.apps.permission_command",
        ]
        settings.ROOT_URLCONF = __name__

        settings.SPARROW_PERMISSION_REGISTER_CONF = {
            "PERMISSION_SERVICE": {
                "ENV_NAME": "PERMISSION_SERVICE_HOST",
                "VALUE": "xxxxx-svc"
            },
            "API_PATH": "/api/permission_i/register/"
        }
        settings.SERVICE_CONF = {
            "NAME": "permiss"
        }
        settings.CONSUL_CLIENT_ADDR = {
            "HOST": os.environ.get("CONSUL_IP", "127.0.0.1"),  # 在k8s上的环境变量类型：变量/变量引用
            "PORT": os.environ.get("CONSUL_PORT", 8500)
        }



