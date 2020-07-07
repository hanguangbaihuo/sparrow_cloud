# -*- coding: utf-8 -*-
"""
requests 的封装， 返回的原生数据

"""
import requests
import logging
from django.conf import settings
from sparrow_cloud.utils.build_url import build_url
from requests.exceptions import ConnectTimeout, ConnectionError, ReadTimeout

logger = logging.getLogger(__name__)


def get_settings_service_name():
    """获取settings中的配置"""
    value = getattr(settings, 'SERVICE_CONF', '')
    if value == '':
        return ''
    service_name = value.get('NAME', '')
    return service_name


def request(method, service_address, api_path, timeout, protocol="http", token=None, *args, **kwargs):
    service_name = get_settings_service_name()
    request_url = build_url(protocol=protocol, address=service_address, api_path=api_path)
    headers = kwargs.get('headers', {})
    if token:
        headers.update({'Authorization': "token " + token})
    try:
        res = requests.request(method=method, url=request_url, timeout=timeout, headers=headers, *args, **kwargs)
        return res
    except Exception as ex:
        error_message = "rest_client error, service_name:{}, protocol:{}, method:{}, " \
                        "request_service_address:{}, api_path:{}, message:{}" \
            .format(service_name, protocol, method, service_address, api_path, ex.__str__())
        logger.error(error_message)
        raise Exception(error_message)


def get(service_address, api_path, timeout=10, token=None, *args, **kwargs):
    return request(method='get', service_address=service_address, api_path=api_path, timeout=timeout, token=token,
                   *args, **kwargs)


def post(service_address, api_path, timeout=10, token=None, *args, **kwargs):
    return request(method='post', service_address=service_address, api_path=api_path, timeout=timeout, token=token,
                   *args, **kwargs)


def put(service_address, api_path, timeout=10, token=None, *args, **kwargs):
    return request(method='put', service_address=service_address, api_path=api_path, timeout=timeout, token=token,
                   *args, **kwargs)


def delete(service_address, api_path, timeout=10, token=None, *args, **kwargs):
    return request(method='delete', service_address=service_address, api_path=api_path, timeout=timeout, token=token,
                   *args, **kwargs)