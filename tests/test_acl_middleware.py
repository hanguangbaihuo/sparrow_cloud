# import os
# import jwt
# import time
# import unittest
# from django.conf import settings
# from django.test import RequestFactory
# from sparrow_cloud.middleware.acl_middleware import ACLMiddleware
# from django.http import JsonResponse
#
#
# os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
#
#
# def token():
#     private_key = settings.PRIVATE_KEY
#     payload = {
#         "service_name": 'test',
#         "ALL": 1,
#         "permission": [],
#         "exp": int(time.time() + 60*60),
#         "iat": int(time.time()),
#         "iss": "ACL"
#     }
#     acl_token = jwt.encode(payload, private_key, algorithm='RS256')
#     return acl_token
#
#
# class TestACLMiddleware(unittest.TestCase):
#     rf = RequestFactory()
#     TOKEN = token()
#
#     def setUp(self):
#         os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
#
#     def test_acl(self):
#         """测试 没有remote_user 和错误的 acl token """
#         request = self.rf.get('/acl', {'acl_token': '123dsafsafaq321dsknfdsj358q744'})
#         self.assertEqual(ACLMiddleware().process_request(request).status_code,
#                          JsonResponse({"message": "ACL验证未通过"}, status=403).status_code)
#
#     def test_acl1(self):
#         """测试 没有remote_user 和正确的 acl token """
#         request = self.rf.get('/acl', {'acl_token': self.TOKEN})
#         self.assertEqual(ACLMiddleware().process_request(request), None)
#
#     def test_acl2(self):
#         """测试 有remote_user 和正确的 acl token """
#         rf1 = RequestFactory(REMOTE_USER='sssssssss')
#         request = rf1.get('/acl', {'acl_token': self.TOKEN})
#         self.assertEqual(ACLMiddleware().process_request(request), None)
#
#     def test_acl3(self):
#         """测试 有remote_user 和错误的 acl token """
#         rf1 = RequestFactory(REMOTE_USER='sssssssss')
#         request = rf1.get('/acl', {'acl_token': '123dsafsafaq321dsknfdsj358q744'})
#         self.assertEqual(ACLMiddleware().process_request(request).status_code,
#                          JsonResponse({"message": "ACL验证未通过"}, status=403).status_code)
#
#     def test_acl4(self):
#         """测试 没有 acl token """
#         request = self.rf.get('/acl')
#         self.assertEqual(ACLMiddleware().process_request(request), None)
#
#     def tearDown(self):
#         del os.environ["DJANGO_SETTINGS_MODULE"]
#
#
# if __name__ == '__main__':
#     unittest.main()
