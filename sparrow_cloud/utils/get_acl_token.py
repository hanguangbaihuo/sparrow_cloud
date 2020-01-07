import time
import logging
import requests
from django.conf import settings
from django.core.cache import cache
from sparrow_cloud.utils.build_url import build_url
from sparrow_cloud.utils.get_hash_key import get_hash_key
from sparrow_cloud.registry.service_discovery import consul_address
from requests.exceptions import ConnectTimeout, ConnectionError
from sparrow_cloud.utils.get_settings_value import get_settings_value

logger = logging.getLogger(__name__)


def requests_get(service_conf, service_name, api_path, timeout=5, retry_times=3):
    """
    service_conf: 服务配置
    :param service_conf:
    :param api_path:
    :param args:
    :param kwargs:
    :return:
    """
    error_message = None
    address_list = consul_address(service_conf)
    exclude_addr = []
    _address = None
    for _ in range(int(retry_times)):
        if len(address_list) > 1:
            [address_list.remove(_) for _ in exclude_addr if _ in address_list]
        try:
            url, address = build_url(address_list, api_path)
            _address = address
            res = requests.get(url, params={'service_name': service_name}, timeout=timeout)
            return res
        except (ConnectionError, ConnectTimeout)as ex:
            exclude_addr.append(_address)
            error_message = ex.__str__()
            logger.error('ACL_SERVICE error, api_path:{}, message: {}, retry:{}'
                         .format(api_path, error_message, int(_)+1))
    raise Exception('ACL_SERVICE error, api_path:{}, message: {}'.format(api_path, error_message))


def get_acl_token(service_name):
    """get service acl token"""
    acl_token_key = get_hash_key()
    settings_acl_token = getattr(settings, acl_token_key, None)
    if settings_acl_token and (int(time.time()) - int(settings_acl_token['time'])) <= int(60*10):
        logging.info('sparrow_cloud: get acl_token from settings, within ten minutes')
        return settings_acl_token['acl_token']
    cache_acl_token = cache.get(acl_token_key)
    if cache_acl_token and (int(time.time()) - int(cache_acl_token['time'])) <= int(60*10):
        logging.info('sparrow_cloud: get acl_token from cache, within ten minutes')
        return cache_acl_token['acl_token']
    acl_middleware = get_settings_value('ACL_MIDDLEWARE')
    try:
        response = requests_get(acl_middleware['ACL_SERVICE'], service_name, acl_middleware['API_PATH'])
        acl_token = response.json()['acl_token']
        setattr(settings, acl_token_key, {'acl_token': acl_token, 'time': time.time()})
        cache.set(acl_token_key, {'acl_token': acl_token, 'time': time.time()})
        logging.info('sparrow_cloud: get acl_token from acl_service')
        return acl_token
    except Exception as ex:
        if cache_acl_token and (int(time.time()) - int(cache_acl_token['time'])) < int(24*60*60):
            logging.info('sparrow_cloud: get acl_token from cache, within 24 hours')
            return cache_acl_token['acl_token']
        if settings_acl_token and (int(time.time()) - int(settings_acl_token['time'])) < int(24*60*60):
            logging.info('sparrow_cloud: get acl_token from settings, within 24 hours')
            return settings_acl_token['acl_token']
        logger.error('sparrow_cloud error: ACL_SERVICE Exception, no token available in cache, message:{}'
                     .format(ex.__str__()))
        raise Exception('sparrow_cloud error: ACL_SERVICE Exception, no token available in cache, message:{}'
                        .format(ex.__str__()))
