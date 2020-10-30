import unittest
from unittest import mock
from sparrow_cloud.service_log.sender import send_log
import os


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

    @mock.patch('requests.request', side_effect=mocked_requests)
    def test_send_log(self, mock_post):
        from django.conf import settings
        settings.SPARROW_SERVICE_LOG_CONF = {
            "SERVICE_LOG": "sparrow-log-svc:8001",
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

    @mock.patch('requests.request', side_effect=mocked_requests1)
    def test_send_log_1(self, mock_post):
        from django.conf import settings
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

    @mock.patch('requests.request', side_effect=mocked_requests1)
    def test_send_log_key_error(self, mock_post):
        from django.conf import settings
        settings.SERVICE_CONF = {
            "NAME": "sparrow_cloud",
        }
        try:
            send_log("key_error")
        except Exception as ex:
            self.assertEqual(type(ex), TypeError)
