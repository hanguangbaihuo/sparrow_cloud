from django.conf import settings
from sparrow_cloud.auth.user import User
from sparrow_cloud.middleware.tracing_middleware import TracingMiddleware
from unittest import mock
import jwt
import logging
import opentracing
import os
import time
import unittest


logger = logging.getLogger(__name__)
# USER_ID = '1112313123'
# PAYLOAD = {"uid": "1112313123", "app_id": "app_0000",
#            "exp": int(time.time()+60*60), "iat": int(time.time()), "iss": "backend"}
# AUTH = b'Token '+jwt.encode(PAYLOAD, '123131313', algorithm='HS256')
# USER = User(user_id=USER_ID)


class MockRequest(object):
    META = {}
    headers = {
        'X-Forwarded-For': '61.149.122.243', 
        'X-Forwarded-Proto': 'https', 
        'X-Envoy-External-Address': '61.149.122.243', 
        'X-Request-Id': 'fcfd868e-591b-9baa-8fdd-25190ba078e1', 
        'Content-Length': '0', 
        'X-B3-Traceid': 'bc85db3a8ad708f324b1c9dcbdd43ba7', 
        'X-B3-Spanid': 'b4939d5270c065f6', 
        'X-B3-Parentspanid': '24b1c9dcbdd43ba7', 
        'X-B3-Sampled': '1'
    }
    method = 'GET'

    def get_full_path(self):
        return 'full_path'


def my_test_view():
    pass


class TestTracing(unittest.TestCase):

    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
        self.tracing_middleware = TracingMiddleware()
        self.global_tracer = opentracing.global_tracer()

    def test_process_view(self):
        self.assertEqual(self.tracing_middleware.process_view(MockRequest(), my_test_view), None)
        # span = self.global_tracer.active_span

    def tearDown(self):
        del os.environ["DJANGO_SETTINGS_MODULE"]


if __name__ == '__main__':
    unittest.main()
