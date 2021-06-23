import os
import json
import logging

from django.conf import settings
from django.core.cache import cache

from sparrow_cloud.utils.get_hash_key import get_hash_key
from sparrow_cloud.utils.get_cm_value import get_cm_value
from sparrow_cloud.utils.get_settings_value import get_settings_value
from sparrow_cloud.restclient import rest_client, requests_client

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
        if os.environ.get("SC_SKIP_TOKEN_CACHE", "").title() != "True":
            cache_user_token = cache.get(user_token_key)
            if cache_user_token:
                return cache_user_token
        # 跳过缓存或者缓存数据空
        data = {
            "name": service_conf["NAME"],
            "secret": service_conf["SECRET"],
            "uid": user_id
        }
        res = requests_client.post(service_address=sc_manage_svc, api_path=sc_manage_api, json=data)
        if res.status_code<200 or res.status_code>=300:
            raise Exception(f"请求app_manage服务出错，状态码:{res.status_code},数据:{res.text}")
        cache.set(user_token_key, res.text, timeout=res.json().get("expires_in", 7200))
        return res.text
    except Exception as ex:
        logger.error(f"sparrowcloud/get_user_token error, no token available in cache and app_manage_error,\
                        'message:{ex.__str__()}, return static token")
        return json.dumps({"iss":"sparrow_cloud", "uid":user_id, "type": "user"})
        # raise Exception('sparrowcloud/get_user_token error, no token available in cache and app_manage_error, '
                        # 'message:{}'.format(ex.__str__()))


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
        if os.environ.get("SC_SKIP_TOKEN_CACHE", "").title() != "True":
            cache_app_token = cache.get(app_token_key)
            if cache_app_token:
                return cache_app_token
        # 跳过缓存或者缓存数据空
        data = {
            "name": service_conf["NAME"],
            "secret": service_conf["SECRET"]
        }
        res = requests_client.post(service_address=sc_manage_svc, api_path=sc_manage_api, json=data)
        if res.status_code<200 or res.status_code>=300:
            raise Exception(f"请求app_manage服务出错，状态码:{res.status_code},数据:{res.text}")
        cache.set(app_token_key, res.text, timeout=res.json().get("expires_in", 7200))
        # logger.info("sparrowcloud get app token: {}".format(app_token["token"]))
        return res.text
    except Exception as ex:
        logger.error(f"sparrowcloud/get_app_token error, no token available in cache and app_manage_error,\
                        'message:{ex.__str__()}, return static token")
        return json.dumps({"iss":"sparrow_cloud", "uid":service_conf["NAME"], "type": "app"})
        # raise Exception('sparrowcloud/get_app_token error, no token available in cache and app_manage_error, '
        #                 'message:{}'.format(ex.__str__()))


