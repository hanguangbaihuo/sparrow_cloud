import json
import logging
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.utils.module_loading import import_string
from rest_framework.settings import api_settings
from sparrow_cloud.restclient import rest_client
from sparrow_cloud.restclient.exception import HTTPException
import requests
import traceback
from pprint import pprint

logger = logging.getLogger(__name__)

'''
settings 配置:

SPARROW_PERMISSION_REGISTER_CONF = {
    "PERMISSION_SERVICE": "test-svc:8000"
    "API_PATH": "/api/permission_i/register/"
}
'''

def get_service_name():
    service_conf = settings.SERVICE_CONF
    service_name = service_conf.get("NAME")
    return service_name


def get_schema(generator, request, public):
    return generator.get_schema(request=request, public=public)


def get_schema_generator(generator_class_name, api_name, api_version):
    generator_class = import_string(generator_class_name)
    return generator_class(
        name=api_name,
        version=api_version
    )


def register(api_list):
    sparrow_permission_register_conf = settings.SPARROW_PERMISSION_REGISTER_CONF
    api_path = sparrow_permission_register_conf['API_PATH']
    permission_service_conf = sparrow_permission_register_conf["PERMISSION_SERVICE"]
    try:
        rest_client.post(permission_service_conf, api_path, json=api_list)
        print("api 注册成功")
    except HTTPException as ex:
        print("api 注册失败. message={}, service_name={}".format(ex.detail, "SPARROW_PERMISSION_REGISTER_NAME"))



