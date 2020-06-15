import unittest
from unittest import mock
import django
from rest_framework.exceptions import PermissionDenied
from django.conf.urls import url
from django.http import HttpResponse
from django.test import RequestFactory
from sparrow_cloud.access_control.decorators import access_control_fbv, access_control_cbv_dispatch, access_control_cbv_method
import os


urlpatterns = []

CONSUL_RETURN_DATA = (
    "name",
    [
        {'ServiceAddress': '162.23.7.247', 'ServicePort': 8001},
        {'ServiceAddress': '142.27.4.252', 'ServicePort': 8001},
        {'ServiceAddress': '122.21.8.131', 'ServicePort': 8001},
    ]
)


# This method will be used by the mock to replace requests.post
def mocked_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, content):
            # self.json_data = json_data
            self.status_code = status_code
            self.content = content

        def json(self):
            return self.content
    if kwargs["params"]["user_id"] == "sssssssss" and kwargs["params"]["resource_code"] == "example1_admin":
        return MockResponse(content={"has_perm": True}, status_code=200)
    elif kwargs["params"]["user_id"] != "sssssssss" or kwargs["params"]["resource_code"] != "example1_admin":
        return MockResponse(content=None, status_code=403)
    return MockResponse(content=None,  status_code=400)


class RestClientTestCase(unittest.TestCase):
    rf = RequestFactory()

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
                    url(r'^/verify/$', detail),
                    ]
                )

    @mock.patch('consul.Consul.Catalog.service', return_value=CONSUL_RETURN_DATA)
    @mock.patch('requests.request', side_effect=mocked_requests)
    @mock.patch('sparrow_cloud.restclient.rest_client.get_acl_token', return_value='123')
    def test_access_control_fbv_200(self, mock_get_acl_token, mock_request, mock_consul):
        def detail1(request):
            return HttpResponse("ok")
        rf1 = RequestFactory(REMOTE_USER='sssssssss')
        request = rf1.get('/verify/')
        decorator = access_control_fbv(resource="permission_example1")(detail1)(request)
        self.assertEqual(decorator.status_code, 200)

    @mock.patch('consul.Consul.Catalog.service', return_value=CONSUL_RETURN_DATA)
    @mock.patch('requests.request', side_effect=mocked_requests)
    @mock.patch('sparrow_cloud.restclient.rest_client.get_acl_token', return_value='123')
    def test_access_control_fbv_403(self, mock_get_acl_token, mock_request, mock_consul):
        def detail1(request):
            return HttpResponse("ok")
        rf1 = RequestFactory(REMOTE_USER='xxx')
        request = rf1.get('/verify/')
        try:
            access_control_fbv(resource="permission_example1")(detail1)(request)
        except Exception as ex:
            self.assertEqual(type(ex), type(PermissionDenied()))

    def tearDown(self):
        pass

    def setup_settings(self, settings):
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
            "ACCESS_CONTROL_CLASS": "sparrow_cloud.apps.access_control.example_access_control.ExampleAccessControl",
            "SECRET": "fdsafgxckrewkrjfvlxosdg",
            "APP_NAME": "test_app"
        }
        settings.SERVICE_CONF = {
            "NAME": "test"
        }