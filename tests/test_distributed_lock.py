import os
import unittest
from unittest import mock
from sparrow_cloud.restclient.exception import HTTPException
from django.test import RequestFactory
from sparrow_cloud.distributed_lock.lock_op import add_lock, remove_lock


MOCK_SUCC_RESPONSE = {"code": 0, "message": "success"}
MOCK_LOCK_FAIL_RESPONSE = {"code": -1, "message": "lock exist"}
MOCK_ERROR_RESPONSE = {"message": "bad request"}

def mocked_requests(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code, content):
            self.json_data = json_data
            self.status_code = status_code
            self.content = content

        def json(self):
            return self.json_data
    return MockResponse(json_data=None, content={"code": 0, "message": "success"},  status_code=200)


class TestAddLock(unittest.TestCase):
    """test 分布式锁 client 加锁"""
    rf = RequestFactory()

    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"

    @mock.patch('sparrow_cloud.restclient.rest_client.post', return_value=MOCK_SUCC_RESPONSE)
    def test_add_lock_succ(self, request):
        res = add_lock("testkey", 100)
        self.assertEqual(res.get("code"), 0)

    @mock.patch('sparrow_cloud.restclient.rest_client.post', return_value=MOCK_LOCK_FAIL_RESPONSE)
    def test_add_lock_fail(self, request):
        res = add_lock("testkey", 100)
        self.assertEqual(res.get("code"), -1)

    @mock.patch('sparrow_cloud.restclient.rest_client.post', return_value=MOCK_ERROR_RESPONSE)
    def test_add_lock_error(self, request):
        try:
            res = add_lock("", "100")
            self.assertEqual(res.get("code"), None)
        except Exception as ex:
            self.assertEqual(type(ex), TypeError)

class TestRemoveLock(unittest.TestCase):
    """test 分布式锁 client 移除锁"""
    rf = RequestFactory()

    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
    
    @mock.patch('sparrow_cloud.restclient.rest_client.delete', return_value=MOCK_SUCC_RESPONSE)
    def test_remove_lock_succ(self, request):
        res = remove_lock("testkey")
        self.assertEqual(res.get("code"), 0)

    @mock.patch('sparrow_cloud.restclient.rest_client.delete', return_value=MOCK_LOCK_FAIL_RESPONSE)
    def test_remove_lock_fail(self, request):
        res = remove_lock("testkey")
        self.assertEqual(res.get("code"), -1)

    @mock.patch('sparrow_cloud.restclient.rest_client.delete', return_value=MOCK_ERROR_RESPONSE)
    def test_remove_lock_error(self, request):
        res = remove_lock("testkey")
        self.assertEqual(res.get("code"), None)