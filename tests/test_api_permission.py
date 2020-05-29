# import unittest
# import os
# from django.conf import settings
# from unittest import mock
# from django.http import JsonResponse
#
#
# class MockRequests(object):
#     @property
#     def path(self):
#         return '/api/xx/xxx/xxxx/'
#
#     @property
#     def method(self):
#         return 'GET'
#
#     @property
#     def META(self):
#         return {'REMOTE_USER': '3213321131312313'}
#
#
# class MockRequests2(object):
#     @property
#     def path(self):
#         return '/api/xx/xxx/123/'
#
#     @property
#     def method(self):
#         return 'GET'
#
#     @property
#     def META(self):
#         return {'REMOTE_USER': '3213321131312313'}
#
#
# class MockRequests1(object):
#     @property
#     def path(self):
#         return '/api/xx/xxx/500/'
#
#     @property
#     def method(self):
#         return 'GET'
#
#     @property
#     def META(self):
#         return {'REMOTE_USER': '3213321131312313'}
#
#
# def mocked_requests_get(*args, **kwargs):
#     class MockResponse:
#         def __init__(self, json_data, status_code):
#             self.json_data = json_data
#             self.status_code = status_code
#
#         def json(self):
#             return self.json_data
#
#         def content(self):
#             return b''
#
#     if kwargs['url'] == 'http://127.0.0.1:8500/api/xx/xxx/xxxx/':
#         return MockResponse({"has_perm": True}, 200)
#     if kwargs['url'] == 'http://127.0.0.1:8500/api/xx/xxx/500/':
#         return MockResponse({"has_perm": False}, 500)
#     return MockResponse({"has_perm": False}, 400)
#
#
# class TestPermissionMiddleware(unittest.TestCase):
#     """测试permission_middleware"""
#     def setUp(self):
#         os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
#         os.environ["SPARROW_TEST_HOST"] = "127.0.0.1:8500"
#
#     @mock.patch('requests.request', side_effect=mocked_requests_get)
#     @mock.patch('sparrow_cloud.utils.validation_data.VerificationConfiguration.valid_permission_svc', return_value='')
#     @mock.patch('sparrow_cloud.restclient.rest_client.get_acl_token', return_value='123')
#     def test_has_permission(self, acl_token, verify_middleware_location, mocked_requests_get):
#         settings.PERMISSION_MIDDLEWARE = {
#             # 权限验证服务的配置
#             "PERMISSION_SERVICE": {
#                 "ENV_NAME": "SPARROW_TEST_HOST",
#                 # VALUE 为服务发现的注册名称
#                 "VALUE": "sparrow",
#             },
#             "API_PATH": "/api/xx/xxx/xxxx/",
#             "FILTER_PATH": [''],  # 使用权限验证中间件， 如有不需要验证的URL， 可添加到列表中
#             "SKIP_PERMISSION": False,
#             # 是否启用权限中间件， SKIP_PERMISSION:True, 则跳过中间件， 如果不配置SKIP_PERMISSION，或者SKIP_PERMISSION:False，则不跳过中间件
#         }
#         from sparrow_cloud.middleware.api_permission import PermissionMiddleware
#         self.assertEqual(PermissionMiddleware().process_request(MockRequests()), None)
#
#     @mock.patch('requests.request', side_effect=mocked_requests_get)
#     @mock.patch('sparrow_cloud.utils.validation_data.VerificationConfiguration.valid_permission_svc', return_value='')
#     @mock.patch('sparrow_cloud.restclient.rest_client.get_acl_token', return_value='123')
#     def test_permission_exception_400(self, acl_token, verify_middleware_location, mocked_requests_get):
#         settings.PERMISSION_MIDDLEWARE = {
#             # 权限验证服务的配置
#             "PERMISSION_SERVICE": {
#                 "ENV_NAME": "SPARROW_TEST_HOST",
#                 # VALUE 为服务发现的注册名称
#                 "VALUE": "sparrow",
#             },
#             "API_PATH": "/api/xx/xxx/ssss/",
#             "FILTER_PATH": [''],  # 使用权限验证中间件， 如有不需要验证的URL， 可添加到列表中
#             "SKIP_PERMISSION": False,
#             # 是否启用权限中间件， SKIP_PERMISSION:True, 则跳过中间件， 如果不配置SKIP_PERMISSION，或者SKIP_PERMISSION:False，则不跳过中间件
#         }
#         from sparrow_cloud.middleware.api_permission import PermissionMiddleware
#         self.assertEqual(PermissionMiddleware().process_request(MockRequests2()).status_code,
#                          JsonResponse({'msg': '400'}, status=400).status_code)
#
#     @mock.patch('requests.request', side_effect=mocked_requests_get)
#     @mock.patch('sparrow_cloud.utils.validation_data.VerificationConfiguration.valid_permission_svc', return_value='')
#     @mock.patch('sparrow_cloud.restclient.rest_client.get_acl_token', return_value='123')
#     def test_permission_exception_500(self, acl_token, verify_middleware_location, mocked_requests_get):
#         settings.PERMISSION_MIDDLEWARE = {
#             # 权限验证服务的配置
#             "PERMISSION_SERVICE": {
#                 "ENV_NAME": "SPARROW_TEST_HOST",
#                 # VALUE 为服务发现的注册名称
#                 "VALUE": "sparrow",
#             },
#             "API_PATH": "/api/xx/xxx/500/",
#             "FILTER_PATH": [''],  # 使用权限验证中间件， 如有不需要验证的URL， 可添加到列表中
#             "SKIP_PERMISSION": False,
#             # 是否启用权限中间件， SKIP_PERMISSION:True, 则跳过中间件， 如果不配置SKIP_PERMISSION，或者SKIP_PERMISSION:False，则不跳过中间件
#         }
#         from sparrow_cloud.middleware.api_permission import PermissionMiddleware
#         PermissionMiddleware().process_request(MockRequests())
#         self.assertEqual(PermissionMiddleware().process_request(MockRequests1()), None)
#
#     @mock.patch('requests.request', side_effect=mocked_requests_get)
#     @mock.patch('sparrow_cloud.utils.validation_data.VerificationConfiguration.valid_permission_svc', return_value='')
#     @mock.patch('sparrow_cloud.restclient.rest_client.get_acl_token', return_value='123')
#     def test_permission_skip_permission_and_filter_path(self, acl_token, verify_middleware_location,
#                                                         mocked_requests_get):
#         settings.PERMISSION_MIDDLEWARE = {
#             # 权限验证服务的配置
#             "PERMISSION_SERVICE": {
#                 "ENV_NAME": "SPARROW_TEST_HOST",
#                 # VALUE 为服务发现的注册名称
#                 "VALUE": "sparrow",
#             },
#             "API_PATH": "/api/xx/xxx/xxxx/",
#             "FILTER_PATH": ['/api/xx/xxx/xxxx/'],  # 使用权限验证中间件， 如有不需要验证的URL， 可添加到列表中
#             "SKIP_PERMISSION": 'False',
#             # 是否启用权限中间件， SKIP_PERMISSION:True, 则跳过中间件， 如果不配置SKIP_PERMISSION，或者SKIP_PERMISSION:False，则不跳过中间件
#         }
#         from sparrow_cloud.middleware.api_permission import PermissionMiddleware
#         PermissionMiddleware().process_request(MockRequests())
#         self.assertEqual(PermissionMiddleware().process_request(MockRequests()), None)
#
#     def tearDown(self):
#         del os.environ["DJANGO_SETTINGS_MODULE"]
#
#
# if __name__ == '__main__':
#     unittest.main()
