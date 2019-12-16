# -*- coding: utf-8 -*-


"""
requests 的封装， 返回的原生数据

"""
import requests
import logging
from django.conf import settings
from sparrow_cloud.utils.build_url import build_url
from sparrow_cloud.utils.get_acl_token import get_acl_token
from requests.exceptions import ConnectTimeout, ConnectionError

logger = logging.getLogger(__name__)


def get_settings_service_name():
    """获取settings中的配置"""
    value = getattr(settings, 'SERVICE_CONF', '')
    if value == '':
        return ''
    service_name = value.get('NAME', '')
    return service_name


def get(service_conf, api_path, timeout=10, retry_times=3, *args, **kwargs):
    """
    service_conf: 服务配置
    :param service_conf:
    :param api_path:
    :param args:
    :param kwargs:
    :return:
    """
    error_message = None
    service_name = get_settings_service_name()
    headers = {'acl_token': get_acl_token(service_name)}
    for _ in range(int(retry_times)):
        try:
            url = build_url(service_conf, api_path)
            res = requests.get(url, headers=headers,  timeout=timeout, *args, **kwargs)
            return res
        except (ConnectionError, ConnectTimeout)as ex:
            error_message = ex.__str__()
            logger.error("requests_client error,service_name:{}, api_path:{}, message:{}, retry:{}".format(service_name,
                                                                                                           api_path,
                                                                                                           error_message,
                                                                                                           int(_)+1))
    raise Exception("requests_client error, service_name: {}, api_path:{}, message: {}".format(service_name, api_path,
                                                                                               error_message))


def post(service_conf, api_path, timeout=10, retry_times=3, *args, **kwargs):
    """
    service_conf: settings 里面配置的服务注册 key 值
    :param service_conf:
    :param api_path:
    :param args:
    :param kwargs:
    :return:
    """
    error_message = None
    service_name = get_settings_service_name()
    headers = {'acl_token': get_acl_token(service_name)}
    for _ in range(int(retry_times)):
        try:
            url = build_url(service_conf, api_path)
            res = requests.post(url, headers=headers, timeout=timeout, *args, **kwargs)
            return res
        except (ConnectionError, ConnectTimeout)as ex:
            error_message = ex.__str__()
            logger.error("requests_client error,service_name:{}, api_path:{}, message:{}, retry:{}".format(service_name,
                                                                                                           api_path,
                                                                                                           error_message,
                                                                                                           int(_)+1))
    raise Exception("requests_client error, service_name: {}, api_path:{}, message: {}".format(service_name, api_path,
                                                                                               error_message))


def put(service_conf, api_path, timeout=10, retry_times=3, *args, **kwargs):
    """
    :param service_conf: settings 里面配置的服务注册 key 值
    :param api_path:
    :param timeout:
    :param args:
    :param kwargs:
    :return:
    """
    error_message = None
    service_name = get_settings_service_name()
    headers = {'acl_token': get_acl_token(service_name)}
    for _ in range(int(retry_times)):
        try:
            url = build_url(service_conf, api_path)
            res = requests.put(url, headers=headers, timeout=timeout, *args, **kwargs)
            return res
        except (ConnectionError, ConnectTimeout)as ex:
            error_message = ex.__str__()
            logger.error("requests_client error,service_name:{}, api_path:{}, message:{}, retry:{}".format(service_name,
                                                                                                           api_path,
                                                                                                           error_message,
                                                                                                           int(_)+1))
    raise Exception("requests_client error, service_name: {}, api_path:{}, message: {}".format(service_name, api_path,
                                                                                               error_message))


def delete(service_conf, api_path, timeout=10, retry_times=3, *args, **kwargs):
    """

    :param service_conf: settings 里面配置的服务注册 key 值
    :param api_path:
    :param timeout:
    :param args:
    :param kwargs:
    :return:
    """
    error_message = None
    service_name = get_settings_service_name()
    headers = {'acl_token': get_acl_token(service_name)}
    for _ in range(int(retry_times)):
        try:
            url = build_url(service_conf, api_path)
            res = requests.delete(url, headers=headers, timeout=timeout, *args, **kwargs)
            return res
        except (ConnectionError, ConnectTimeout)as ex:
            error_message = ex.__str__()
            logger.error("requests_client error,service_name:{}, api_path:{}, message:{}, retry:{}".format(service_name,
                                                                                                           api_path,
                                                                                                           error_message,
                                                                                                           int(_)+1))
    raise Exception("requests_client error, service_name: {}, api_path:{}, message: {}".format(service_name, api_path,
                                                                                               error_message))

