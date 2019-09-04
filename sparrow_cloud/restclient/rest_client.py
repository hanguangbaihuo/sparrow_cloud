# -*- coding: utf-8 -*-

import requests
from sparrow_cloud.registry.service_discovery import consul_service
from .exception import HTTPException



def get(service_settings_key, api_path, *args, **kwargs):
    '''
    service_settings_key: settings 里面配置的服务注册 key 值
    '''
    url = _build_url(service_settings_key, api_path)
    res = requests.get(url, *args, **kwargs)
    return _handle_response(res)

def post(service_settings_key, api_path, *args, **kwargs):
    '''
    service_settings_key: settings 里面配置的服务注册 key 值
    '''
    url = _build_url(service_settings_key, api_path)
    # import pdb; pdb.set_trace()
    res = requests.post(url, *args, **kwargs)
    return _handle_response(res)


def _build_url(service_settings_key, api_path):
    servicer_addr = consul_service(service_settings_key)
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
