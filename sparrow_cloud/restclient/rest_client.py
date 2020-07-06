# -*- coding: utf-8 -*-

import os
import requests
import logging
import opentracing
from django.conf import settings
from sparrow_cloud.utils.build_url import build_url
from .exception import HTTPException

logger = logging.getLogger(__name__)


def get_settings_service_name():
    """获取settings中的配置"""
    value = getattr(settings, 'SERVICE_CONF', '')
    if value == '':
        return ''
    service_name = value.get('NAME', '')
    return service_name


def request(method, service_address, api_path, timeout, protocol="http", *args, **kwargs):
    headers = kwargs.pop('headers', {})
    # tracing
    tracer = opentracing.global_tracer()
    if tracer:
        span = tracer.active_span
        if span:
            carrier = {}
            tracer.inject(span, opentracing.Format.HTTP_HEADERS, carrier)
            headers.update(carrier)
            logger.debug('=================== carrier: {}'.format(carrier))
    # find service
    service_name = get_settings_service_name()
    request_url = build_url(protocol=protocol, address=service_address, api_path=api_path)
    try:
        res = requests.request(method=method, url=request_url, timeout=timeout, headers=headers, *args, **kwargs)
        return _handle_response(res)
    except Exception as ex:
        error_message = "rest_client error, service_name:{}, request_service_address:{},  message:{}"\
            .format(service_name, request_url, ex.__str__())
        logger.error(error_message)
        logging.info("rest_client is called, service_name:{}, protocol:{}, method:{}, request_service_address:{}, "
                     "api_path:{}".format(service_name, protocol, method, service_address, api_path))
        raise HTTPException(error_message)


def get(service_address, api_path, timeout=10, *args, **kwargs):
    return request('get', service_address, api_path, timeout, *args, **kwargs)


def post(service_address, api_path, timeout=10, *args, **kwargs):
    return request('post', service_address, api_path, timeout, *args, **kwargs)


def put(service_address, api_path, timeout=10, *args, **kwargs):
    return request('put', service_address, api_path, timeout, *args, **kwargs)


def delete(service_address, api_path, timeout=10, *args, **kwargs):
    return request('delete', service_address, api_path, timeout, *args, **kwargs)


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