import os
import json
import logging

from django.conf import settings
from django.core.cache import cache

from sparrow_cloud.utils.get_hash_key import get_hash_key
from sparrow_cloud.utils.get_cm_value import get_cm_value
from sparrow_cloud.utils.get_settings_value import get_settings_value
from sparrow_cloud.restclient import rest_client

logger = logging.getLogger(__name__)


def get_user_token(user_id):
    """
    get user token
    :param user_id:
    
    configmap：
        SC_MANAGE_SVC
        SC_MANAGE_API
    """
    user_token_key = get_hash_key(key_type="user", user_id=user_id)
    service_conf = get_settings_value("SERVICE_CONF")
    sc_manage_svc = get_cm_value("SC_MANAGE_SVC")
    sc_manage_api = get_cm_value("SC_MANAGE_API")
    try:
        cache_user_token = cache.get(user_token_key)
        if cache_user_token is not None:
            return cache_user_token["user_token"]["token"]
        else:
            data = {
                "name": service_conf["NAME"],
                "secret": service_conf["SECRET"],
                "uid": user_id
            }
            user_token = rest_client.post(service_address=sc_manage_svc, api_path=sc_manage_api, json=data)
            cache.set(user_token_key, {'user_token': user_token}, timeout=user_token["expires_in"]-120)
            logger.info("sparrowcloud get user token: {}".format(user_token["token"]))
            return user_token["token"]
    except Exception as ex:
        raise Exception('sparrowcloud/get_user_token error, no token available in cache and app_manage_error, '
                        'message:{}'.format(ex.__str__()))


def get_app_token():
    """
    get app token
    configmap：
        SC_MANAGE_SVC
        SC_MANAGE_API
    """
    app_token_key = get_hash_key(key_type="app")
    service_conf = get_settings_value("SERVICE_CONF")
    sc_manage_svc = get_cm_value("SC_MANAGE_SVC")
    sc_manage_api = get_cm_value("SC_MANAGE_API")
    try:
        cache_app_token = cache.get(app_token_key)
        if cache_app_token:
            return cache_app_token["app_token"]["token"]
        else:
            data = {
                "name": service_conf["NAME"],
                "secret": service_conf["SECRET"]
            }
            app_token = rest_client.post(service_address=sc_manage_svc, api_path=sc_manage_api, json=data)
            cache.set(app_token_key, {'app_token': app_token}, timeout=app_token["expires_in"]-120)
            logger.info("sparrowcloud get app token: {}".format(app_token["token"]))
            return app_token["token"]
    except Exception as ex:
        raise Exception('sparrowcloud/get_app_token error, no token available in cache and app_manage_error, '
                        'message:{}'.format(ex.__str__()))


