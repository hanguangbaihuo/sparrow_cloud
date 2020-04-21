import unittest
from unittest import mock
from sparrow_cloud.service_log.sender import send_log
import os


CONSUL_RETURN_DATA = (
    "name",
    [
        {'ServiceAddress': '162.23.7.247', 'ServicePort': 8001},
        {'ServiceAddress': '142.27.4.252', 'ServicePort': 8001},
        {'ServiceAddress': '122.21.8.131', 'ServicePort': 8001},
    ]
)


def mocked_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, content):
            self.json_data = json_data
            self.status_code = status_code
            self.content = content

        def json(self):
            return self.json_data
    return MockResponse(json_data=None, content=None,  status_code=200)


def mocked_requests1(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, content):
            self.json_data = json_data
            self.status_code = status_code
            self.content = content

        def json(self):
            return self.json_data
    return MockResponse(json_data=None, content=None,  status_code=500)


class ServiceLogCase(unittest.TestCase):

    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"

    @mock.patch('consul.Consul.Catalog.service', return_value=CONSUL_RETURN_DATA)
    @mock.patch('requests.request', side_effect=mocked_requests)
    @mock.patch('sparrow_cloud.restclient.requests_client.get_acl_token', return_value='123')
    def test_send_log(self, token, mock_post, consul):
        from django.conf import settings
        settings.SPARROW_SERVICE_LOG_CONF = {
            "SERVICE_LOG": {
                "ENV_NAME": "SPARROW_SERVICE_LOG",
                "VALUE": os.environ.get("SPARROW_SERVICE_LOG", "sparrow-service-log-svc"),
            },
            "PATH": "/service_log/log/",
        }
        settings.SERVICE_CONF = {
            "NAME": "sparrow_cloud",
        }
        data = {
            "object_id": "test_object_id",
            "object_name": "test_object_name",
            "user_id": "888888889",
            "user_name": "tiger",
            "user_phone": "18700000401",
            "action": "跑路啦",
            "message": "enenenenenenenenene"
        }

        res = send_log(data)
        self.assertEqual(res, True)

    @mock.patch('consul.Consul.Catalog.service', return_value=CONSUL_RETURN_DATA)
    @mock.patch('requests.request', side_effect=mocked_requests1)
    @mock.patch('sparrow_cloud.restclient.requests_client.get_acl_token', return_value='123')
    def test_send_log(self, token, mock_post, consul):
        from django.conf import settings
        settings.SPARROW_SERVICE_LOG_CONF = {
            "SERVICE_LOG": {
                "ENV_NAME": "SPARROW_SERVICE_LOG",
                "VALUE": os.environ.get("SPARROW_SERVICE_LOG", "sparrow-service-log-svc"),
            },
            "PATH": "/service_log/log/",
        }
        settings.SERVICE_CONF = {
            "NAME": "sparrow_cloud",
        }
        data = {
            "object_id": "test_object_id",
            "object_name": "test_object_name",
            "user_id": "888888889",
            "user_name": "tiger",
            "user_phone": "18700000401",
            "action": "跑路啦",
            "message": "enenenenenenenenene"
        }
        res = send_log(data)
        self.assertEqual(res, False)

    @mock.patch('consul.Consul.Catalog.service', return_value=CONSUL_RETURN_DATA)
    @mock.patch('requests.request', side_effect=mocked_requests1)
    @mock.patch('sparrow_cloud.restclient.requests_client.get_acl_token', return_value='123')
    def test_send_log_key_error(self, token, mock_post, consul):
        from django.conf import settings
        settings.SPARROW_SERVICE_LOG_CONF = {
            "SERVICE_LOG": {
                "ENV_NAME": "SPARROW_SERVICE_LOG",
                "VALUE": os.environ.get("SPARROW_SERVICE_LOG", "sparrow-service-log-svc"),
            },
            "PATH": "/service_log/log/",
        }
        settings.SERVICE_CONF = {
            "NAME": "sparrow_cloud",
        }
        try:
            send_log("key_error")
        except Exception as ex:
            self.assertEqual(type(ex), TypeError)
