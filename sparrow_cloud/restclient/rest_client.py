# -*- coding: utf-8 -*-

import requests
from sparrow_cloud.registry.service_registry import consul_service
from .exception import HTTP5XXException, HTTP4XXException, HTTPException



def get(service_conf, api_path, data=None, *args, **kwargs):
    '''
    service_conf: 服务配置
        {
            "SERVICE_NAME": "xxxxxx",   # 服务名称
            "NAME_SVC": "xxxxxx_svc",   # consul 服务发现中心的注册名字
            "HOST": "127.0.0.1:8500",   # 本地配置, 可以覆盖 consul
        }
    '''
    servicer_addr = consul_service(service_conf)
    url = _build_url(service_conf, api_path)
    res = requests.get(url, data=data *args, **kwargs)
    return _handle_response(res)

def post(service_conf, api_path, data=None, *args, **kwargs):
    '''
    service_conf: 服务配置
        {
            "SERVICE_NAME": "xxxxxx",   # 服务名称
            "NAME_SVC": "xxxxxx_svc",   # consul 服务发现中心的注册名字
            "HOST": "127.0.0.1:8500",   # 本地配置, 可以覆盖 consul
        }
    '''
    servicer_addr = consul_service(service_conf)
    url = _build_url(service_conf, api_path)
    res = requests.post(url, data=data *args, **kwargs)
    return _handle_response(res)


def _build_url(service_conf, api_path):
    servicer_addr = consul_service(service_conf)
    return "{}{}".format(servicer_addr, api_path)


def _handle_response(response):
    if res.status_code >= 500:
        raise HTTP5XXException(
            code=res.status_code,
            detail=res.content
        )
    elif res.status_code >=400:
        raise HTTP4XXException(
            code=res.status_code,
            detail=res.json()
        )
    elif res.status_code >=200:
        res_result = res.json()
        res_result['status_code'] = res.status_code
        return res_result
    elif:
        raise HTTPException(
            code=res.status_code,
            detail=res.content
        )