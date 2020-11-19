import os
import unittest
from unittest import mock
from sparrow_cloud.restclient.exception import HTTPException
from django.test import RequestFactory
from sparrow_cloud.app_message.sender import send_message


MOCK_RESPONSE = {"code": 0, "message": "发送成功", "data": ""}

RESPONSE_CONTENT = {
    "group_code_list": [
        "group_code_list 传递错误"
    ]
}


def mocked_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, content):
            self.json_data = json_data
            self.status_code = status_code
            self.content = content

        def json(self):
            return self.json_data
    return MockResponse(json_data=None, content={"code": 0, "message": "success"},  status_code=200)

class TestAppMessage(unittest.TestCase):
    """ly message client"""
    rf = RequestFactory()

    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"

    @mock.patch('sparrow_cloud.restclient.rest_client.post', return_value=MOCK_RESPONSE)
    def test_send_message_text(self, request):
        res = send_message(msg_data={"content": "1505"}, code_type="bowen_test")
        self.assertEqual(res, {"code": 0, "message": "发送成功", "data": ""})

    @mock.patch('sparrow_cloud.restclient.rest_client.post', return_value=MOCK_RESPONSE)
    def test_send_message_text1(self, request):
        res = send_message(msg_data={"content": "1505"}, code_type="bowen_test", msg_sender="测试",shop_id="2")
        self.assertEqual(res, {"code": 0, "message": "发送成功", "data": ""})

    @mock.patch('sparrow_cloud.restclient.rest_client.post', return_value=MOCK_RESPONSE)
    def test_send_message_image(self, request):
        res = send_message(msg_data={"url": "http://www.test.com/image"}, code_type="bowen_test", content_type="image", msg_sender="测试")
        self.assertEqual(res, {"code": 0, "message": "发送成功", "data": ""})

    @mock.patch('sparrow_cloud.restclient.rest_client.post', return_value=MOCK_RESPONSE)
    def test_send_message_image1(self, request):
        res = send_message(msg_data={"url": "http://www.test.com/image"}, code_type="bowen_test", content_type="image", msg_sender="测试", shop_id="2")
        self.assertEqual(res, {"code": 0, "message": "发送成功", "data": ""})