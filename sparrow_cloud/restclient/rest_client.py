# -*- coding: utf-8 -*-
import json
import logging
import requests
import opentracing
from sparrow_cloud.utils.build_url import build_url
from sparrow_cloud.utils.get_settings_value import get_service_name
from .exception import HTTPException

logger = logging.getLogger(__name__)


def request(method, service_address, api_path, timeout, protocol="http", token=None, *args, **kwargs):
    '''
    :param method: method for the new :class:`Request` object.
    :param service_address: service name, e.g. sparrow-product-svc:8001
    :param api_path: reqeust url
    :param timeout: (optional) How many seconds to wait for the server to send data
        before giving up, as a float, or a :ref:`(connect timeout, read
        timeout) <timeouts>` tuple.
    :param token: should be a json format dict or json string, it should be
        {'uid': '1234abc', 'exp': 1722200316, 'iat': 1622193116, 'app_id': 'core'} type
        encode token by `json.dumps` to request header X-Jwt-Payload
    :param kwargs:
    :param headers: (optional) Dictionary of HTTP Headers to send
    '''
    service_name = get_service_name()
    request_url = build_url(protocol=protocol, address=service_address, api_path=api_path)
    headers = kwargs.pop('headers', {})
    if token:
        if isinstance(token, dict): #token also should contain "uid" key
            headers.update({'X-Jwt-Payload': json.dumps(token)})
        elif isinstance(token, str):
            headers.update({'X-Jwt-Payload': token})
        else:
            logger.error(f"rest_client token parameter is not suitable type: {token}")
    tracer = opentracing.global_tracer()
    if tracer:
        span = tracer.active_span
        if span:
            carrier = {}
            tracer.inject(span, opentracing.Format.HTTP_HEADERS, carrier)
            headers.update(carrier)
            # logger.debug('=================== carrier: {}'.format(carrier))
    try:
        res = requests.request(method=method, url=request_url, headers=headers, timeout=timeout, *args, **kwargs)
        return _handle_response(res)
    except Exception as ex:
        error_message = "rest_client error, service_name:{}, protocol:{}, method:{}, " \
                        "request_service_address:{}, api_path:{}, message:{}"\
            .format(service_name, protocol, method, service_address, api_path, ex.__str__())
        logger.error(error_message)
        raise HTTPException(error_message)


def get(service_address, api_path, timeout=30, token=None, *args, **kwargs):
    return request(method='get', service_address=service_address, api_path=api_path, timeout=timeout, token=token,
                   *args, **kwargs)


def post(service_address, api_path, timeout=30, token=None, *args, **kwargs):
    return request(method='post', service_address=service_address, api_path=api_path, timeout=timeout, token=token,
                   *args, **kwargs)


def put(service_address, api_path, timeout=30, token=None, *args, **kwargs):
    return request(method='put', service_address=service_address, api_path=api_path, timeout=timeout, token=token,
                   *args, **kwargs)


def patch(service_address, api_path, timeout=30, token=None, *args, **kwargs):
    return request(method='patch', service_address=service_address, api_path=api_path, timeout=timeout, token=token,
                   *args, **kwargs)


def delete(service_address, api_path, timeout=30, token=None, *args, **kwargs):
    return request(method='delete', service_address=service_address, api_path=api_path, timeout=timeout, token=token,
                   *args, **kwargs)


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