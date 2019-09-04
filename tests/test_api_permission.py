import unittest
from unittest import mock

MOCK_SERVICE_DATA= {
    "NAME": "sparrow",
    "HOST": "",
    "PORT": 8001,
    "PATH": "/api/xx/xxx/xxxx/"
}


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
    @mock.patch("sparrow_cloud.restclient.rest_client.consul_service", return_value="127.0.0.1:8500")
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('sparrow_cloud.utils.get_settings_value.GetSettingsValue.get_middleware_value', return_value=MOCK_SERVICE_DATA)
    @mock.patch('sparrow_cloud.utils.get_settings_value.GetSettingsValue.get_value', return_value=False)
    @mock.patch('sparrow_cloud.utils.get_settings_value.GetSettingsValue.get_middleware_value', return_value=[])
    @mock.patch('sparrow_cloud.utils.validation_data.VerificationConfiguration.valid_permission_svc', return_value='')
    def test_has_permission(self, verify_middleware_location, get_middleware_value, get_value, middleware_value,
                        mocked_requests_get, mock_consul_service):
        from sparrow_cloud.middleware.api_permission import PermissionMiddleware
        self.assertEqual(PermissionMiddleware().process_request(MockRequests()), None)

    

if __name__ == '__main__':
    unittest.main()
