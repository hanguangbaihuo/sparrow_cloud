# -*- coding: utf-8 -*-

import os
import django
import unittest

from unittest import mock
from requests.exceptions import ConnectionError, ReadTimeout
from sparrow_cloud.restclient import rest_client
from django.conf import settings


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


def mocked_requests_read_timeout(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, content):
            self.json_data = json_data
            self.status_code = status_code
            self.content = content
    raise ReadTimeout


def mocked_requests_connection_error(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, content):
            self.json_data = json_data
            self.status_code = status_code
            self.content = content

        def json(self):
            return self.json_data
    raise ConnectionError


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
        res = rest_client.post(service_address, API_PATH, data=DATA)
        self.assertEqual(res, {'key1': 'value1'})

    @mock.patch('requests.request', side_effect=mocked_requests)
    def test_put(self, mock_put):
        service_address = settings.SERVICE_ADDRESS
        res = rest_client.put(service_address, API_PATH, data=DATA)
        self.assertEqual(res, {'key1': 'value1'})

    @mock.patch('requests.request', side_effect=mocked_requests)
    def test_get(self, mock_get):
        service_address = settings.SERVICE_ADDRESS
        res = rest_client.get(service_address, API_PATH, data=DATA)
        self.assertEqual(res, {'key1': 'value1'})

    @mock.patch('requests.request', side_effect=mocked_requests)
    def test_delete(self, mock_delete):
        service_address = settings.SERVICE_ADDRESS
        res = rest_client.delete(service_address, API_PATH, data=DATA)
        self.assertEqual(res, {'key1': 'value1'})

    @mock.patch('requests.request', side_effect=mocked_requests_empty_data)
    def test_empty_data(self, mock_get):
        service_address = settings.SERVICE_ADDRESS
        res = rest_client.get(service_address, API_PATH)
        self.assertEqual(res, {})

    @mock.patch('requests.request', side_effect=mocked_requests_not_empty_data)
    def test_empty_data_err(self, mock_get):
        service_address = settings.SERVICE_ADDRESS
        res = rest_client.get(service_address, API_PATH)
        self.assertEqual(res, {'data': {'key2': 'value2'}, 'message': "'MockResponse' object has no attribute 'json'"})

    @mock.patch('requests.request', side_effect=mocked_requests_read_timeout)
    def test_post_err(self, mock_post):
        service_address = settings.SERVICE_ADDRESS
        try:
            rest_client.post(service_address, API_PATH, data=DATA)
        except Exception as ex:
            message = ex.__str__()
            self.assertEqual(message, 'rest_client error, service_name:sparrow_cloud, protocol:http, method:post, '
                                      'request_service_address:sparrow-test-svc:8000, api_path:/api/xxx/, message:')

    @mock.patch('requests.request', side_effect=mocked_requests_connection_error)
    def test_put_err(self, mock_put):
        service_address = settings.SERVICE_ADDRESS
        try:
            rest_client.put(service_address, API_PATH, data=DATA)
        except Exception as ex:
            message = ex.__str__()
            self.assertEqual(message, 'rest_client error, service_name:sparrow_cloud, protocol:http, method:put, '
                                      'request_service_address:sparrow-test-svc:8000, api_path:/api/xxx/, message:')

    def setup_settings(self, settings):
        settings.SERVICE_ADDRESS = SERVICE_ADDRESS
        settings.SERVICE_CONF = {"NAME": "sparrow_cloud"}

    def tearDown(self):
        del os.environ["DJANGO_SETTINGS_MODULE"]
