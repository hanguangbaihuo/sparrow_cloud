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


def request(method, service_address, api_path, timeout, protocol="http", *args, **kwargs):
    service_name = get_settings_service_name()
    request_url = build_url(protocol=protocol, address=service_address, api_path=api_path)
    try:
        res = requests.request(method=method, url=request_url, timeout=timeout, *args, **kwargs)
        return res
    except Exception as ex:
        error_message = "request_client error, service_name:{}, request_service_address:{},  message:{}" \
            .format(service_name, request_url, ex.__str__())
        logger.error(error_message)
        logging.info("requests_client is called, service_name:{}, protocol:{}, method:{}, request_service_address:{}, "
                     "api_path:{}".format(service_name, protocol, method, service_address, api_path))
        raise Exception(error_message)


def get(service_address, api_path, timeout=10, *args, **kwargs):
    return request('get', service_address, api_path, timeout, *args, **kwargs)


def post(service_address, api_path, timeout=10, *args, **kwargs):
    return request('post', service_address, api_path, timeout, *args, **kwargs)


def put(service_address, api_path, timeout=10, *args, **kwargs):
    return request('put', service_address, api_path, timeout, *args, **kwargs)


def delete(service_address, api_path, timeout=10, *args, **kwargs):
    return request('delete', service_address, api_path, timeout, *args, **kwargs)