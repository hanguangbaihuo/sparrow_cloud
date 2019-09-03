import unittest
from unittest import mock


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://127.0.0.1:9999/api':
        return MockResponse({"status": True, "message": "成功", }, 200)
    return MockResponse({"status": False, "message": "失败"}, 200)


class MockRequests(object):
    @property
    def path(self):
        return '/api/test/1'

    @property
    def method(self):
        return 'GET'

    @property
    def META(self):
        return {'REMOTE_USER': '3213321131312313'}


class TestPermissionMiddleware(unittest.TestCase):
    """测试permission_middleware"""

    @mock.patch('sparrow_cloud.utils.validation_data.VerificationConfiguration.verify_middleware_location',
                return_value='')
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('sparrow_cloud.utils.validation_data.VerificationConfiguration.valid_permission_svc',
                return_value='')
    @mock.patch('django.conf.settings', return_value='')
    @mock.patch('sparrow_cloud.utils.normalize_url.NormalizeUrl.normalize_url',
                return_value='http://127.0.0.1:9999/api')
    def test_have_authority(self, NormalizeUrl, settings, valid_permission_svc, requests, verify_middleware_location):
        from sparrow_cloud.middleware.api_permissiong import PermissionMiddleware
        self.assertEqual(PermissionMiddleware().process_request(MockRequests()), None)


if __name__ == '__main__':
    unittest.main()