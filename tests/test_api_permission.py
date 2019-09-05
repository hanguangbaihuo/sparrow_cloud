import unittest
import os
from django.conf import settings
from unittest import mock


class MockRequests(object):
    @property
    def path(self):
        return '/api/xx/xxx/xxxx/'

    @property
    def method(self):
        return 'GET'

    @property
    def META(self):
        return {'REMOTE_USER': '3213321131312313'}


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
        
        def content(self):
            return b''

    if args[0] == 'http://127.0.0.1:8500/api/xx/xxx/xxxx/':
        return MockResponse({"has_perm": True}, 200)
    return MockResponse({"has_perm": False}, 404)


class TestPermissionMiddleware(unittest.TestCase):
    """测试permission_middleware"""
    def setUp(self):
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.mock_settings"
        settings.PERMISSION_MIDDLEWARE = {
            # 权限验证服务的配置
            "PERMISSION_SERVICE": {
                "NAME": "sparrow",  # 服务名称（k8s上的服务名）, 必填
                "HOST": "",  # IP, 开发环境必填（开发环境使用转发到本地的host）
                "PORT": 8001,  # 服务端口, dev环境需要注意， 配置写的端口需要和转发到本地的端口保持一致, 必填
                "PATH": "/api/xx/xxx/xxxx/",  # url, 必填
            },
            "FILTER_PATH": [''],  # 使用权限验证中间件， 如有不需要验证的URL， 可添加到列表中
            "SKIP_PERMISSION": False,
            # 是否启用权限中间件， SKIP_PERMISSION:True, 则跳过中间件， 如果不配置SKIP_PERMISSION，或者SKIP_PERMISSION:False，则不跳过中间件
        }

    @mock.patch("sparrow_cloud.restclient.rest_client.consul_service", return_value="127.0.0.1:8500")
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('sparrow_cloud.utils.validation_data.VerificationConfiguration.valid_permission_svc', return_value='')
    def test_has_permission(self, verify_middleware_location, mocked_requests_get, mock_consul_service):
        from sparrow_cloud.middleware.api_permission import PermissionMiddleware
        self.assertEqual(PermissionMiddleware().process_request(MockRequests()), None)


    def tearDown(self):
        # import pdb; pdb.set_trace()
        del os.environ["DJANGO_SETTINGS_MODULE"]

if __name__ == '__main__':
    unittest.main()
