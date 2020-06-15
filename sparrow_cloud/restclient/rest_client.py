# -*- coding: utf-8 -*-

import requests
import logging
import opentracing
from django.conf import settings
from opentracing.propagation import Format
from sparrow_cloud.utils.build_url import build_url
from sparrow_cloud.utils.get_acl_token import get_acl_token
from sparrow_cloud.registry.service_discovery import consul_address
from requests.exceptions import ConnectTimeout, ConnectionError, ReadTimeout
from .exception import HTTPException


logger = logging.getLogger(__name__)


def get_settings_service_name():
    """获取settings中的配置"""
    value = getattr(settings, 'SERVICE_CONF', '')
    if value == '':
        return ''
    service_name = value.get('NAME', '')
    return service_name


def request(method, service_conf, api_path, timeout, retry_times, *args, **kwargs):
    headers = kwargs.get('headers', {})
    # tracing
    tracer = opentracing.global_tracer()
    if tracer:
        span = tracer.active_span
        if span:
            carrier = {}
            tracer.inject(span, Format.HTTP_HEADERS, carrier)
            headers.update(carrier)
    # find service
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
            res = requests.request(
                method=method, url=url, timeout=timeout, headers=headers, *args, **kwargs)
            return _handle_response(res)
        except (ConnectionError, ConnectTimeout, ReadTimeout)as ex:
            exclude_addr.append(_address)
            error_message = ex.__str__()
            logger.error("rest_client error,service_name:{}, request_service:{}, api_path:{}, message:{}, retry:{}"
                         .format(service_name, request_service, api_path, error_message, int(_) + 1))
    raise Exception("rest_client error, service_name: {}, request_service:{}, api_path:{}, message: {}"
                    .format(service_name, request_service, api_path, error_message))


def get(service_conf, api_path, timeout=10, retry_times=3, *args, **kwargs):
    return request('get', service_conf, api_path, timeout, retry_times, *args, **kwargs)


def post(service_conf, api_path, timeout=10, retry_times=3, *args, **kwargs):
    return request('post', service_conf, api_path, timeout, retry_times, *args, **kwargs)


def put(service_conf, api_path, timeout=10, retry_times=3, *args, **kwargs):
    return request('put', service_conf, api_path, timeout, retry_times, *args, **kwargs)


def delete(service_conf, api_path, timeout=10, retry_times=3, *args, **kwargs):
    return request('delete', service_conf, api_path, timeout, retry_times, *args, **kwargs)


def _handle_response(response):
    if 200 <= response.status_code < 300:
        if response.content:
            try:
                res_result = response.json()
            except Exception as ex:
                res_result = {
                    "data": response.content,
                    "message": str(ex),
                }
        else:
            res_result = {}
        return res_result
    else:
        xx = HTTPException(
            code="http_exception",
            detail=response.content,
        )
        xx.status_code = response.status_code
        raise xx
