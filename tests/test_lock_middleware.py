import os
import unittest
from unittest import mock
from sparrow_cloud.middleware.lock_middleware import CheckLockMiddleware

class MockRequest(object):
    META = {"HTTP_SC_LOCK":"exist"}

class MockEmptyRequest(object):
    META = {"HTTP_SC_LOCK":""}

class MockNoRequest(object):
    META = {}

class MockResponse(object):
    status_code = 200
    def json():
        return {"message":"ok"}
    
class MockWrongResponse(object):
    status_code = 400
    def json():
        return {"message":"some error occur"}

class TestLockMiddleware(unittest.TestCase):

    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
        self.middleware = CheckLockMiddleware()

    @mock.patch('sparrow_cloud.restclient.rest_client.put', return_value={"code":0})
    def test_process_request_1(self,allow_mock):
        # 测试header中携带前端锁的key，且锁服务返回正常
        self.assertEqual(self.middleware.process_request(MockRequest()),None)

    @mock.patch('sparrow_cloud.restclient.rest_client.put', return_value={"code":1})
    def test_process_request_2(self,deny_mock):
        # 测试header中携带前端锁的key，且锁服务返回拒绝本次请求
        response = self.middleware.process_request(MockRequest())
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"code", response.content)
        self.assertIn(b"233402", response.content)

    @mock.patch('sparrow_cloud.restclient.rest_client.put', return_value={"code":0})
    def test_process_request_3(self,empty_header):
        # 测试header中携带前端锁的key为空情况，且锁服务返回正常
        self.assertEqual(self.middleware.process_request(MockEmptyRequest()),None)

    @mock.patch('sparrow_cloud.restclient.rest_client.put', return_value={"code":0})
    def test_process_request_4(self,no_header):
        # 测试header中不携带前端锁的key，且锁服务返回正常
        self.assertEqual(self.middleware.process_request(MockNoRequest()),None)

    @mock.patch('sparrow_cloud.restclient.rest_client.delete', return_value={"code":0})
    def test_process_response_1(self, header):
        # 测试header中携带前端锁的key，response处理返回正常
        response = self.middleware.process_response(MockRequest(), MockResponse())
        self.assertEqual(response.status_code, 200)

    @mock.patch('sparrow_cloud.restclient.rest_client.put', return_value={"code":0})
    def test_process_response_2(self, header):
        # 测试header中携带前端锁的key，response处理返回异常
        response = self.middleware.process_response(MockRequest(), MockWrongResponse())
        self.assertEqual(response.status_code, MockWrongResponse().status_code)
    
    @mock.patch('sparrow_cloud.restclient.rest_client.delete', return_value={"code":0})
    def test_process_response_3(self, no_header):
        # 测试header中不携带前端锁的key，response处理返回正常
        response = self.middleware.process_response(MockNoRequest(), MockResponse())
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        del os.environ["DJANGO_SETTINGS_MODULE"]


if __name__ == '__main__':
    unittest.main()