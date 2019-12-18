import os
import unittest
from django.test import RequestFactory
from sparrow_cloud.middleware.acl_middleware import ACLMiddleware
from django.http import JsonResponse

TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhY2xfdGVzdCI6InBheWxvYWQifQ.q4cU3UmAI_F85mgKsi_fdqr8xweCuaKzYLlV" \
        "mUVajiOOtoA27enRXkAAdB9FsmCf2JeHOtuFnFUsQj24Car4H4Gm26MFz-divqQTdroSv-uflaBje3Thh6okRpG7ZhTzyGOpbdSLmKL3r" \
        "FGalZJISplO6OIcCPupiuGGuVDWpAU"


class TestACLMiddleware(unittest.TestCase):
    rf = RequestFactory()

    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"

    def test_acl(self):
        """测试 没有remote_user 和错误的 acl token """
        request = self.rf.get('/acl', {'acl_token': '123dsafsafaq321dsknfdsj358q744'})
        self.assertEqual(ACLMiddleware().process_request(request).status_code,
                         JsonResponse({"message": "ACL验证未通过"}, status=403).status_code)

    def test_acl1(self):
        """测试 没有remote_user 和正确的 acl token """
        request = self.rf.get('/acl', {'acl_token': TOKEN})
        self.assertEqual(ACLMiddleware().process_request(request), None)

    def test_acl2(self):
        """测试 有remote_user 和正确的 acl token """
        rf1 = RequestFactory(REMOTE_USER='sssssssss')
        request = rf1.get('/acl', {'acl_token': TOKEN})
        self.assertEqual(ACLMiddleware().process_request(request), None)

    def test_acl3(self):
        """测试 有remote_user 和错误的 acl token """
        rf1 = RequestFactory(REMOTE_USER='sssssssss')
        request = rf1.get('/acl', {'acl_token': '123dsafsafaq321dsknfdsj358q744'})
        self.assertEqual(ACLMiddleware().process_request(request).status_code,
                         JsonResponse({"message": "ACL验证未通过"}, status=403).status_code)

    def test_acl4(self):
        """测试 没有 acl token """
        request = self.rf.get('/acl')
        self.assertEqual(ACLMiddleware().process_request(request), None)

    def tearDown(self):
        del os.environ["DJANGO_SETTINGS_MODULE"]


if __name__ == '__main__':
    unittest.main()
