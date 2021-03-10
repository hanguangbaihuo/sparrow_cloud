# -*- coding: utf-8 -*-
"""
requests 的封装， 返回的原生数据

"""
import requests
import logging
import opentracing

from sparrow_cloud.utils.build_url import build_url
from sparrow_cloud.utils.get_settings_value import get_service_name

logger = logging.getLogger(__name__)


def request(method, service_address, api_path, protocol="http", token=None, *args, **kwargs):
    service_name = get_service_name()
    request_url = build_url(protocol=protocol, address=service_address, api_path=api_path)
    headers = kwargs.pop('headers', {})
    if token:
        headers.update({'Authorization': "token " + token})
    tracer = opentracing.global_tracer()
    if tracer:
        span = tracer.active_span
        if span:
            carrier = {}
            tracer.inject(span, opentracing.Format.HTTP_HEADERS, carrier)
            headers.update(carrier)
            # logger.debug('=================== carrier: {}'.format(carrier))
    try:
        res = requests.request(method=method, url=request_url, headers=headers, *args, **kwargs)
        return res
    except Exception as ex:
        error_message = "rest_client error, service_name:{}, protocol:{}, method:{}, " \
                        "request_service_address:{}, api_path:{}, message:{}" \
            .format(service_name, protocol, method, service_address, api_path, ex.__str__())
        logger.error(error_message)
        raise ex


def get(service_address, api_path, timeout=30, token=None, *args, **kwargs):
    return request(method='get', service_address=service_address, api_path=api_path, timeout=timeout, token=token,
                   *args, **kwargs)


def post(service_address, api_path, timeout=30, token=None, *args, **kwargs):
    return request(method='post', service_address=service_address, api_path=api_path, timeout=timeout, token=token,
                   *args, **kwargs)


def put(service_address, api_path, timeout=30, token=None, *args, **kwargs):
    return request(method='put', service_address=service_address, api_path=api_path, timeout=timeout, token=token,
                   *args, **kwargs)


def delete(service_address, api_path, timeout=30, token=None, *args, **kwargs):
    return request(method='delete', service_address=service_address, api_path=api_path, timeout=timeout, token=token,
                   *args, **kwargs)