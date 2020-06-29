# import unittest
# from unittest import mock
# import django
# from io import StringIO
# from django.core.management import call_command
# import os
# from django.conf.urls import url
# from django.http import HttpResponse
#
#
# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)
#
#
# urlpatterns = [
#     url(r'^/ssss/xxx/$', detail),
#     url(r'^/ssuuu/xxddx/$', detail),
# ]
#
#
# class RestClientTestCase(unittest.TestCase):
#
#     def setUp(self):
#         os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
#
#     @mock.patch('sparrow_cloud.restclient.rest_client.post', return_value={})
#     def test_register_command_list(self, mock_post):
#         from django.conf import settings
#         self.setup_settings(settings)
#
#         django.setup()
#         out = StringIO()
#         os.environ["PERMISSION_SERVICE_HOST"] = "127.0.0.1:8001"
#         call_command('register_api_permission', '-d', '2', '-l', stdout=out)
#         self.assertEqual(out.read(), '')
#
#     @mock.patch('sparrow_cloud.restclient.rest_client.post', return_value={})
#     def test_register_command(self, mock_post):
#         from django.conf import settings
#         self.setup_settings(settings)
#         django.setup()
#         out = StringIO()
#         os.environ["PERMISSION_SERVICE_HOST"] = "127.0.0.1:8001"
#         call_command('register_api_permission', '-d', '2', stdout=out)
#         self.assertEqual(out.read(), '')
#
#     def tearDown(self):
#         del os.environ["PERMISSION_SERVICE_HOST"]
#
#     def setup_settings(self, settings):
#         settings.XX = "1"
#         settings.SECRET_KEY = "ss"
#         settings.ROOT_URLCONF = __name__
#
#         settings.SPARROW_PERMISSION_REGISTER_CONF = {
#             "PERMISSION_SERVICE": "test-svc:8000",
#             "API_PATH": "/api/permission_i/register/"
#         }
#         settings.SERVICE_CONF = {
#             "NAME": "permiss"
#         }
#         settings.CONSUL_CLIENT_ADDR = {
#             "HOST": os.environ.get("CONSUL_IP", "127.0.0.1"),  # 在k8s上的环境变量类型：变量/变量引用
#             "PORT": os.environ.get("CONSUL_PORT", 8500)
#         }