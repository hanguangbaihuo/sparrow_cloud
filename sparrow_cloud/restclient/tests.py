import unittest
from client import RestClient
from unittest.mock import patch

'''
Test Case 说明:
domain: api.hg.com

参数            test_case0           test_case1
api            /api/cart/self0/     /api/cart/self0/
method         get                  get
header         {}                   {}
ssl_enable     False
timeout        None
retry          0
payload        {}
query_params   []
uri_params     ["api"]
append_slash   True
返回值          {"key1": "value1"}
描述            测试基础 get
'''

CART_SELF_RETURN = {"self": "self"}
CART_SELF0_RETURN = {"self0": "self0"}
CART_SELF1_RETURN = {"self1": "self1"}

class MockResponse:

        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

# mock get 方法
def mocked_requests_get(*args, **kwargs):
    # class MockResponse:

    #     def __init__(self, json_data, status_code):
    #         self.json_data = json_data
    #         self.status_code = status_code

    #     def json(self):
    #         return self.json_data

    if args[0] == 'http://api.hg.com/api/cart/self/':
        return MockResponse(CART_SELF_RETURN, 200)
    elif args[0] == 'http://api.hg.com/api/cart/self0/':
        return MockResponse(CART_SELF0_RETURN, 200)
    return MockResponse(None, 404)

# mock post 方法
def mocked_requests_post(*args, **kwargs):
    if args[0] == 'http://api.hg.com/api/cart/self1/':
        return MockResponse(CART_SELF1_RETURN, 200)
    # elif args[0] == 'http://api.hg.com/api/cart/self0/':
    #     return MockResponse(CART_SELF0_RETURN, 200)
    return MockResponse(None, 404)


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestWechatBasic(unittest.TestCase):

    domain = "api.hg.com"

    # requests_get_mock_object = MockResponse({}, 200)
    @patch('requests.get', side_effect=mocked_requests_get)
    def test_base(self, requests_get):
        '''
            参数
            api              http://api.hg.com/api/cart/self/
            method           get
            header           {}
            ssl_enable       False
            timeout          None
            retry            0
            payload          {}
            query_params     {}
            uri_params       []
            append_slash     True
            正确返回值: 
                {
                    "key1": "value1"
                }
        '''
        # 初始化
        uri_parts = ["api"]
        ssl_enable = False
        json_res = RestClient(domain=self.domain, 
            uri_parts=uri_parts, ssl_enable=ssl_enable).cart.self(
            http_method='get', headers={}
        )
        self.assertEqual(json_res, CART_SELF_RETURN)

    @patch('requests.get', side_effect=mocked_requests_get)
    def test_get_0(self, requests_get):
        '''
            参数
            api              http://api.hg.com/api/cart/self0/
            method           get
            header           {
                                'Authorization': 'Token dddddd'
                             }
            ssl_enable       False
            timeout          None
            retry            0
            payload          {}
            query_params     {}
            uri_params       []
            append_slash     True
            正确返回值: 
                {
                    "self0": "self0"
                }
        '''
        uri_parts = ["api"]
        ssl_enable = False
        headers = {
            'Authorization': 'Token dddddd'
        }
        json_res = RestClient(domain=self.domain, 
            uri_parts=uri_parts, ssl_enable=ssl_enable).cart.self0(
            http_method='get', headers=headers
        )
        self.assertEqual(json_res, CART_SELF0_RETURN)

    @patch('requests.post', side_effect=mocked_requests_post)
    def test_post_0(self, requests_post):
        '''
            参数
            api              http://api.hg.com/api/cart/self1/
            method           post
            header           {
                                'Authorization': 'Token dddddd'
                             }
            ssl_enable       False
            timeout          None
            retry            0
            payload          {
                               "x": "y"
                             }
            query_params     {}
            uri_params       []
            append_slash     True
            正确返回值: 
                {
                    "self0": "self0"
                }
        '''
        uri_parts = ["api"]
        ssl_enable = False
        headers = {
            'Authorization': 'Token dddddd'
        }
        json_res = RestClient(domain=self.domain, 
            uri_parts=uri_parts, ssl_enable=ssl_enable).cart.self1(
            http_method='post', headers=headers
        )
        self.assertEqual(json_res, CART_SELF1_RETURN)


if __name__ == '__main__':
    unittest.main()