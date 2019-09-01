# -*- coding: utf-8 -*-

import hashlib
import logging
import requests
from urllib.parse import urlencode, quote_plus
from sparrow_cloud.registry.service_registry import consul_service

'''
Rest http to dynimaic function: 把 rest 方法转化为 动态方法调用
    HTTP 请求:
        header: [(key, value), ...]
        query_params: [(key, value), ...]
        payload: {
            key: value
        }
        url: 参数 (value0, value1, value2, ...)
            url 参数占位符: _key_

response: json
    {
        "key": "value"
    }

1 如果 url 里面有参数怎们办?



'''

ALLOWED_HTTP_METHOD = ('get', 'post', 'head', 'options', 'put', 'delete')

URI_PARAMS_PLACEHOLDER = "_key_"

class RestClientException(Exception):
    """
    base exception
    """
    pass

class RestHTTPException(RestClientException):
    pass


class HttpMethodNotAllowedException(Exception):
    """
    微信 请求方法不允许
    """
    def __str__(self):
        message = 'http not allowed'
        return (message)


def get_service_addr(service_conf):
    '''
    获取服务地址
    '''
    if not isinstance(service_conf, dict):
        raise TypeError("service_conf should be Dict. but get {}".format(type(service_conf)))
    service_addr = consul_service(service_conf)
    return service_addr

def build_uri(uri_parts, uri_params, append_slash):
    '''
    使用参数生成url
    kwargs 里面的参数不在这里面生成 uri，这个参数将会作为 requests的参数传入get or post
    如果有的 api 需要使用 kwargs里面的参数，在这里进行特殊处理
    '''

    # 替换掉占位符
    # tempuri_parts = []
    uri_parts_count = uri_parts.count(URI_PARAMS_PLACEHOLDER)
    uri_params_len = len(uri_params)
    # 替换掉 url 参数里面的占位符
    if uri_params:
        if uri_parts_count != uri_params_len:
            raise RestClientException("url参数个数不符合, 需要%s, 实际传入%s" % (uri_parts_count, uri_params_len))
        else:
            j = 0
            for n, i in enumerate(uri_parts):
                if i == URI_PARAMS_PLACEHOLDER:
                    uri_parts[n] = uri_params[j]
                    j += 1
    # 处理查询字符串
    uri = '/'.join(str(x) for x in uri_parts)
    if append_slash:
        uri = uri + "/"
    return uri

def build_query_parmas(query_params):
    if query_params:
        return urlencode(query_params, quote_via=quote_plus)
    else:
        return ""


def check_http_method(http_method):

    if http_method.lower() in ALLOWED_HTTP_METHOD:
        return True 
    else:
        raise HttpMethodNotAllowedException


class RestCall(object):
    '''
    ref：https://github.com/sixohsix/twitter/blob/master/twitter/api.py
    '''

    def __init__(self, callable_cls, service_conf, uri_parts=[],
                 ssl_enable=True, timeout=None, retry=0):
        self.service_conf = service_conf
        self.callable_cls = callable_cls
        # self.uri = uri
        self.uri_parts = uri_parts
        self.timeout = timeout
        self.retry = retry
        self.ssl_enable = ssl_enable

    def out_put(self):
        # print(self.domain)
        # print(self.callable_cls)
        print(self.uri_parts)

    def __getattr__(self, key):
        # self.out_put()
        try:
            return object.__getattr__(self, key)
        except AttributeError:
            # 递归调用，查找属性，每次的调用都将属性值作为一个参数存入 uri_parts
            def extend_call(arg):
                # import pdb; pdb.set_trace()
                # print(arg)
                return self.callable_cls(
                    callable_cls=self.callable_cls,
                    service_conf=self.service_conf, 
                    uri_parts=self.uri_parts + [arg],
                    ssl_enable=self.ssl_enable,
                    timeout=self.timeout, 
                    retry=self.retry)
            return extend_call(key)



    def __call__(self, http_method='get', headers={}, payload={}, 
        query_params=None, uri_params=[], append_slash=True):
        '''
        使父类成为可调用类
        '''
        lower_http_method = http_method.lower()
        check_http_method(lower_http_method)
        uri = build_uri(
            uri_parts=self.uri_parts, 
            uri_params=uri_params, 
            append_slash=append_slash
            )
        # logger.info(uri)
        domain = get_service_addr(self.service_conf)
        # 检查是否使用 https
        secure_str = ''
        if self.ssl_enable:
            secure_str = 's'
        # dot = ""
        # import pdb; pdb.set_trace()
        url = "http%s://%s/%s" % (secure_str, domain, uri)
        query_str = build_query_parmas(query_params)
        if query_str:
            url = url + "?" + query_str
        # import pdb; pdb.set_trace()
        # print("url=%s" % url)
        # print("payload=%s" % payload)
        # print("headers=%s" % headers)
        re = getattr(requests, lower_http_method)(url, json=payload, headers=headers)
        # return re.json()
        return self._handle_response(re=re)


    def _handle_response(self, re):
        try:
            json_data = re.json()
        except Exception as ex:
            raise RestClientException("api return value not json: %s" % re.content)
        if re.status_code > 200:
            raise RestHTTPException("get data error: status_code={0}, message={1}" % (re.status_code, json_data))
        return json_data


class RestClient(RestCall):

    def __init__(self, service_conf, uri_parts=[], ssl_enable=False, timeout=None, retry=0):
        '''
        @ssl_enable: 是否使用 https, 默认使用 http
        @domain: api域名
        @retry : 默认 0, >0, 重试次数
        @uri_parts = ["api", "sparrow_product"]
        @timeout: 请求的超时时间, 无默认值
        '''
        RestCall.__init__(self, 
            service_conf=service_conf, callable_cls=RestCall, uri_parts=uri_parts, 
            ssl_enable=ssl_enable, timeout=timeout, retry=retry)


__all__ = ["RestClient", "RestCall"]

if __name__ == '__main__':
    domain = "backend5.hanguangbaihuo.com"
    # domain = "backend5.hanguangbaihuo.com"
    uri_parts = ["api"]
    headers = {
        'Authorization': 'Token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJjOWU2ZGYwOGRmN2Q0ZDM3ODQxYzgxZTdjNzVhMTFmOSIsImFwcF9pZCI6ImFwcF8xNTIxMDEwNzg4IiwiZXhwIjoxNTY1MTk1Nzk4LCJpYXQiOjE1NjUxMDkzOTgsImlzcyI6ImJhY2tlbmQifQ.T4zIr4WrifZ7g6HV378egHq-BtYI7JTMFzWwS6b8gts'
    }
    backend5_client = RestClient(domain=domain, uri_parts=uri_parts, ssl_enable=True)
    json_res = backend5_client.address.user(http_method='get', headers=headers)
    logger.info(json_res)