import os
import json
import logging
from django.core.cache import cache
from sparrow_cloud.utils.get_hash_key import get_hash_key
from sparrow_cloud.utils.get_settings_value import get_settings_value
from sparrow_cloud.restclient import rest_client

logger = logging.getLogger(__name__)


def get_user_token(user_id):
    """
    get user token
    REGISTRY_APP_CONF = {
        "SERVICE_ADDRESS": "sparrow-service-svc:8000",
        "PATH": "/api/get_app_token/",
        "ENABLE_TOKEN_CACHE": os.environ.get("ENABLE_TOKEN_CACHE", False)
    }
    :param user_id:
    :return:
    """
    user_token_key = get_hash_key(key_type="user", user_id=user_id)
    service_conf = get_settings_value("SERVICE_CONF")
    registry_app_conf = get_settings_value("REGISTRY_APP_CONF")
    enable_get_token_cache = registry_app_conf["ENABLE_TOKEN_CACHE"]
    if enable_get_token_cache:
        cache_user_token = cache.get(user_token_key)
        if cache_user_token:
            return cache_user_token["user_token"]
    try:
        data = {
            "name": service_conf["NAME"],
            "secret": service_conf["SECRET"],
            "uid": user_id
        }
        data_to_send = json.dumps(data).encode("utf-8")
        user_token = rest_client.post(service_address=registry_app_conf["SERVICE_ADDRESS"],
                                      api_path=registry_app_conf["PATH"], timeout=0.5, data=data_to_send)
        cache.set(user_token_key, {'user_token': user_token}, timeout=user_token["expires_in"]-120)
        return user_token
    except Exception as ex:
        raise Exception('get_user_token error, no token available in cache and registry_app_error, '
                        'message:{}'.format(ex.__str__()))


def get_app_token():
    """
    get app token
    REGISTRY_APP_CONF = {
        "SERVICE_ADDRESS": "sparrow-service-svc:8000",
        "PATH": "/api/get_app_token/",
        "ENABLE_TOKEN_CACHE": os.environ.get("ENABLE_TOKEN_CACHE", False)
    }
    :return:
    """
    app_token_key = get_hash_key(key_type="app")
    service_conf = get_settings_value("SERVICE_CONF")
    registry_app_conf = get_settings_value("REGISTRY_APP_CONF")
    enable_get_token_cache = registry_app_conf["ENABLE_TOKEN_CACHE"]
    if enable_get_token_cache:
        cache_app_token = cache.get(app_token_key)
        if cache_app_token:
            return cache_app_token["app_token"]
    try:
        data = {
            "name": service_conf["NAME"],
            "secret": service_conf["SECRET"]
        }
        data_to_send = json.dumps(data).encode("utf-8")
        app_token = rest_client.post(service_address=registry_app_conf["SERVICE_ADDRESS"],
                                     api_path=registry_app_conf["PATH"], timeout=0.5, data=data_to_send)
        cache.set(app_token_key, {'app_token': app_token}, timeout=app_token["expires_in"]-120)
        return app_token
    except Exception as ex:
        raise Exception('get_app_token error, no token available in cache and registry_app_error, '
                        'message:{}'.format(ex.__str__()))


