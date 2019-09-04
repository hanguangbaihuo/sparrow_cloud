# -*- coding: utf-8 -*-

import requests
from sparrow_cloud.registry.service_registry import consul_service
from .exception import HTTPException



def get(service_conf, api_path, *args, **kwargs):
    '''
    service_conf: 服务配置
        {
            "SERVICE_REGISTER_NAME": "xxxxxx_svc",   # consul 服务发现中心的注册名字
            "HOST": "127.0.0.1:8500",   # 本地配置, 可以覆盖 consul
        }
    '''
    servicer_addr = consul_service(service_conf)
    url = _build_url(service_conf, api_path)
    res = requests.get(url, *args, **kwargs)
    return _handle_response(res)

def post(service_conf, api_path, *args, **kwargs):
    '''
    service_conf: 服务配置
        {
            "SERVICE_REGISTER_NAME": "xxxxxx_svc",   # consul 服务发现中心的注册名字
            "HOST": "127.0.0.1:8500",   # 本地配置, 可以覆盖 consul
        }
    '''
    # import pdb; pdb.set_trace()
    servicer_addr = consul_service(service_conf)
    # import pdb; pdb.set_trace()
    url = _build_url(service_conf, api_path)
    res = requests.post(url, *args, **kwargs)
    return _handle_response(res)


def _build_url(service_conf, api_path):
    servicer_addr = consul_service(service_conf)
    return "http://{}{}".format(servicer_addr, api_path)


def _handle_response(response):
    if 200 <= response.status_code < 300:
        res_result = response.json()
        res_result['status_code'] = response.status_code
        return res_result
    else:
        xx = HTTPException(
            code="http_exception",
            detail=response.content,
        )
        xx.status_code = response.status_code
        raise xx
