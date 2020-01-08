# -*- coding: utf-8 -*-
"""
requests 的封装， 返回的原生数据

"""
import requests
import logging
from django.conf import settings
from sparrow_cloud.utils.build_url import build_url
from sparrow_cloud.utils.get_acl_token import get_acl_token
from requests.exceptions import ConnectTimeout, ConnectionError, ReadTimeout
from sparrow_cloud.registry.service_discovery import consul_address

logger = logging.getLogger(__name__)


def get_settings_service_name():
    """获取settings中的配置"""
    value = getattr(settings, 'SERVICE_CONF', '')
    if value == '':
        return ''
    service_name = value.get('NAME', '')
    return service_name


def request(method, service_conf, api_path, timeout, retry_times, *args, **kwargs):
    error_message = None
    service_name = get_settings_service_name()
    request_service = service_conf['VALUE']
    acl_token = get_acl_token(service_name)
    if acl_token is not None:
        params = kwargs.get('params', {})
        params['acl_token'] = acl_token
        kwargs['params'] = params
    address_list = consul_address(service_conf)
    exclude_addr = []
    _address = None
    for _ in range(int(retry_times)):
        if len(address_list) > 1 and isinstance(address_list, list):
            [address_list.remove(_) for _ in exclude_addr if _ in address_list]
        try:
            url, address = build_url(address_list, api_path)
            _address = address
            res = requests.request(method=method, url=url, timeout=timeout, *args, **kwargs)
            return res
        except (ConnectionError, ConnectTimeout, ReadTimeout)as ex:
            exclude_addr.append(_address)
            error_message = ex.__str__()
            logger.error("requests_client error,service_name:{}, request_service:{}, api_path:{}, message:{}, retry:{}"
                         .format(service_name, request_service, api_path, error_message, int(_) + 1))
    raise Exception("requests_client error, service_name: {}, request_service:{}, api_path:{}, message: {}"
                    .format(service_name, request_service, api_path, error_message))


def get(service_conf, api_path, timeout=10, retry_times=3, *args, **kwargs):
    return request('get', service_conf, api_path, timeout, retry_times, *args, **kwargs)


def post(service_conf, api_path, timeout=10, retry_times=3, *args, **kwargs):
    return request('post', service_conf, api_path, timeout, retry_times, *args, **kwargs)


def put(service_conf, api_path, timeout=10, retry_times=3, *args, **kwargs):
    return request('put', service_conf, api_path, timeout, retry_times, *args, **kwargs)


def delete(service_conf, api_path, timeout=10, retry_times=3, *args, **kwargs):
    return request('delete', service_conf, api_path, timeout, retry_times, *args, **kwargs)