# -*- coding: utf-8 -*-
import os
import unittest
import django

from unittest import mock
from django.conf import settings
from sparrow_cloud.restclient import requests_client


# This method will be used by the mock to replace requests.post
def mocked_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, content):
            self.json_data = json_data
            self.status_code = status_code
            self.content = content

        def json(self):
            return self.json_data
    if kwargs['url'].endswith('/api/xxx/'):
        return MockResponse(json_data={"key1": "value1"}, content={'key2': 'value2'},  status_code=200)
    return MockResponse(json_data=None, content=None,  status_code=400)


def mocked_requests_empty_data(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, content):
            self.status_code = status_code
            self.content = content

    if kwargs['url'].endswith('/api/xxx/'):
        return MockResponse(content=None, status_code=200)
    return MockResponse(content=None, status_code=400)


def mocked_requests_not_empty_data(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, content):
            self.status_code = status_code
            self.content = content

    if kwargs['url'].endswith('/api/xxx/'):
        return MockResponse(content={'key2': 'value2'}, status_code=200)
    return MockResponse(content=None, status_code=400)


SERVICE_ADDRESS = "sparrow-test-svc:8000"

API_PATH = "/api/xxx/"
DATA = {"key": "value"}


class RestClientTestCase(unittest.TestCase):

    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
        from django.conf import settings
        self.setup_settings(settings)
        django.setup()

    @mock.patch('requests.request', side_effect=mocked_requests)
    def test_post(self, mock_post):
        service_address = settings.SERVICE_ADDRESS
        res = requests_client.post(service_address, API_PATH, data=DATA)
        self.assertEqual(res.json(), {'key1': 'value1'})

    @mock.patch('requests.request', side_effect=mocked_requests)
    def test_put(self, mock_put):
        service_address = settings.SERVICE_ADDRESS
        res = requests_client.put(service_address, API_PATH, data=DATA)
        self.assertEqual(res.json(), {'key1': 'value1'})

    @mock.patch('requests.request', side_effect=mocked_requests)
    def test_get(self, mock_get):
        service_address = settings.SERVICE_ADDRESS
        res = requests_client.get(service_address, API_PATH, data=DATA)
        self.assertEqual(res.json(), {'key1': 'value1'})

    @mock.patch('requests.request', side_effect=mocked_requests)
    def test_delete(self, mock_delete):
        service_address = settings.SERVICE_ADDRESS
        res = requests_client.delete(service_address, API_PATH, data=DATA)
        self.assertEqual(res.json(), {'key1': 'value1'})

    @mock.patch('requests.request', side_effect=mocked_requests)
    def test_not_acl(self, mock_post):
        service_address = settings.SERVICE_ADDRESS
        res = requests_client.post(service_address, API_PATH, data=DATA)
        self.assertEqual(res.json(), {'key1': 'value1'})

    def tearDown(self):
        del os.environ["DJANGO_SETTINGS_MODULE"]

    def setup_settings(self, settings):
        settings.SERVICE_ADDRESS = SERVICE_ADDRESS