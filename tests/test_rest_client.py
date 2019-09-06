# -*- coding: utf-8 -*-
import unittest
from unittest import mock
from sparrow_cloud.restclient import rest_client
import os


# This method will be used by the mock to replace requests.post
def mocked_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
    if args[0].endswith('/api/xxx/'):
        return MockResponse({"key1": "value1"}, 200)
    # elif args[0] == 'http://someotherurl.com/anothertest.json':
    #     return MockResponse({"key2": "value2"}, 200)

    return MockResponse(None, 404)


CONSUL_RETURN_DATA = (
    "name", 
    [
        {'ServiceAddress': '162.23.7.247', 'ServicePort': 8001,},
        {'ServiceAddress': '142.27.4.252', 'ServicePort': 8001,},
        {'ServiceAddress': '122.21.8.131', 'ServicePort': 8001,},
    ]
)

SERVICE_CONF = {
    "ENV_NAME": "PERMISSION_REGISTER_NAME_HOST",
    "VALUE": "sprrow-permission-svc"
    }


class RestClientTestCase(unittest.TestCase):

    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"

    @mock.patch('consul.Consul.Catalog.service', return_value=CONSUL_RETURN_DATA)
    @mock.patch('requests.post', side_effect=mocked_requests)
    def test_post(self, mock_post, mock_service):
        api_path = "/api/xxx/"
        data = {
            "key": "value",
        }
        from django.conf import settings
        settings.CONSUL_CLIENT_ADDR = {
            "HOST": "127.0.0.1",
            "PORT": 8500
        }
        settings.SERVICE_CONF = SERVICE_CONF
        res = rest_client.post(SERVICE_CONF, api_path, data=data)
        self.assertEqual(res, {'key1': 'value1', 'status_code': 200})


    @mock.patch('consul.Consul.Catalog.service', return_value=CONSUL_RETURN_DATA)
    @mock.patch('requests.get', side_effect=mocked_requests)
    def test_get(self, mock_get, mock_service):
        api_path = "/api/xxx/"
        data = {
            "key": "value",
        }
        from django.conf import settings
        settings.CONSUL_CLIENT_ADDR = {
            "HOST": "127.0.0.1",
            "PORT": 8500
        }
        settings.SERVICE_CONF = SERVICE_CONF
        res = rest_client.get(SERVICE_CONF, api_path, data=data)
        self.assertEqual(res, {'key1': 'value1', 'status_code': 200})

    def tearDown(self):
        # import pdb; pdb.set_trace()
        del os.environ["DJANGO_SETTINGS_MODULE"]
