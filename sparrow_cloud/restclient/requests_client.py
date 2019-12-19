# -*- coding: utf-8 -*-
"""
requests 的封装， 返回的原生数据

"""
import requests
import logging
from sparrow_cloud.utils.build_url import build_url
from sparrow_cloud.utils.get_acl_token import get_acl_token
from django.conf import settings
from requests.exceptions import ConnectTimeout, ConnectionError, ReadTimeout

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
    params = kwargs.get('params', {})
    params['acl_token'] = acl_token
    kwargs['params'] = params
    for _ in range(int(retry_times)):
        try:
            url = build_url(service_conf, api_path)
            res = requests.request(method=method, url=url, timeout=timeout, *args, **kwargs)
            return res
        except (ConnectionError, ConnectTimeout, ReadTimeout)as ex:
            error_message = ex.__str__()
            logger.error("requests_client error,service_name:{}, request_service:{}, api_path:{}, message:{}, retry:{}"
                         .format(service_name, request_service, api_path, error_message, int(_) + 1))
    raise Exception("requests_client error, service_name: {}, request_service:{}, api_path:{}, message: {}"
                    .format(service_name, request_service, api_path, error_message))


def get(service_conf, api_path, timeout=5, retry_times=3, *args, **kwargs):
    return request('get', service_conf, api_path, timeout, retry_times, *args, **kwargs)


def post(service_conf, api_path, timeout=5, retry_times=3, *args, **kwargs):
    return request('post', service_conf, api_path, timeout, retry_times, *args, **kwargs)


def put(service_conf, api_path, timeout=5, retry_times=3, *args, **kwargs):
    return request('put', service_conf, api_path, timeout, retry_times, *args, **kwargs)


def delete(service_conf, api_path, timeout=5, retry_times=3, *args, **kwargs):
    return request('delete', service_conf, api_path, timeout, retry_times, *args, **kwargs)