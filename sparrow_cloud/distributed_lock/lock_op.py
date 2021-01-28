import os
import json
import logging

from django.conf import settings
from sparrow_cloud.restclient.exception import HTTPException
from sparrow_cloud.utils.get_cm_value import get_cm_value
from sparrow_cloud.utils.get_settings_value import get_settings_value
from sparrow_cloud.restclient import rest_client

logger = logging.getLogger(__name__)

sc_distributed_lock_svc = get_cm_value("SC_SPARROW_DISTRIBUTED_LOCK_SVC")
sc_distributed_lock_api = get_cm_value("SC_SPARROW_DISTRIBUTED_LOCK_API")

def add_lock(key:str, expire_time:int, *args, **kwargs):
    """
        # ConfigMap:
            SC_SPARROW_DISTRIBUTED_LOCK_SVC
            SC_SPARROW_DISTRIBUTED_LOCK_API
    """
    service_conf = get_settings_value("SERVICE_CONF")
    service_name = service_conf.get("NAME", None)
    service_secret = service_conf.get("SECRET", None)
    if not service_name or not service_secret:
        raise Exception("NAME or SECRET is not configured in SERVICE_CONF settings")
    data = {
        "service_name": service_name,
        "secret": service_secret,
        "key": key,
        "expire_time": expire_time,
    }
    try:
        res = rest_client.post(sc_distributed_lock_svc, sc_distributed_lock_api, json=data, *args, **kwargs)
        logging.info("sparrow_cloud distributed lock add lock, data:{}".format(data))
        return res
    except HTTPException as ex:
        logging.error("sparrow_cloud distributed lock add lock error: {}".format(ex))
        raise HTTPException(ex)

def remove_lock(key:str, *args, **kwargs):
    """
        # ConfigMap:
            SC_SPARROW_DISTRIBUTED_LOCK_SVC
            SC_SPARROW_DISTRIBUTED_LOCK_API
    """
    service_conf = get_settings_value("SERVICE_CONF")
    service_name = service_conf.get("NAME", None)
    service_secret = service_conf.get("SECRET", None)
    if not service_name or not service_secret:
        raise Exception("NAME or SECRET is not configured in SERVICE_CONF settings")
    data = {
        "service_name": service_name,
        "secret": service_secret,
        "key": key,
    }
    try:
        res = rest_client.delete(sc_distributed_lock_svc, sc_distributed_lock_api, json=data, *args, **kwargs)
        logging.info("sparrow_cloud distributed lock remove lock, data:{}".format(data))
        return res
    except HTTPException as ex:
        logging.error("sparrow_cloud distributed lock remove lock error: {}".format(ex))
        raise HTTPException(ex)
