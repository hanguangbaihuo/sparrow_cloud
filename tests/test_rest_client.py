# -*- coding: utf-8 -*-
import unittest
from unittest import mock
from sparrow_cloud.restclient import rest_client


# This method will be used by the mock to replace requests.post
def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'http://127.0.0.1:8500/api/xxx/':
        return MockResponse({"key1": "value1"}, 200)
    # elif args[0] == 'http://someotherurl.com/anothertest.json':
    #     return MockResponse({"key2": "value2"}, 200)

    return MockResponse(None, 404)


class RestClientTestCase(unittest.TestCase):

    @mock.patch("sparrow_cloud.restclient.rest_client.consul_service", return_value="127.0.0.1:8500")
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_post(self, mock_post, mock_consul_service):
        # 
        service_conf = {
            "SERVICE_REGISTER_NAME": "xxxxxx_svc",   # consul 服务发现中心的注册名字
            "HOST": "127.0.0.1:8500",   # 本地配置, 可以覆盖 consul
        }
        api_path = "/api/xxx/"
        data = {
            "key": "value",
        }
        res = rest_client.post(service_conf, api_path, data=data)
        self.assertEqual(res, {'key1': 'value1', 'status_code': 200})

if __name__ == '__main__':
    unittest.main()
