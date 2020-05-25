import logging
import importlib

from django.core.management.base import BaseCommand

from sparrow_cloud.restclient import rest_client
from sparrow_cloud.utils.common_exceptions import ResourceValidError
from sparrow_cloud.utils.get_settings_value import get_settings_value

logger = logging.getLogger(__name__)


def get_resource_cls(class_path):
    if class_path:
        module_path, cls_name = class_path.rsplit(".", 1)
        try:
            access_control_cls = getattr(importlib.import_module(module_path), cls_name)
        except Exception as ex:
            logging.error('ERROR: access_control incorrect incoming parameters,'
                          'resource:{}, message:{},'.format(class_path, ex.__str__()))
            raise ResourceValidError('ERROR: access_control incorrect incoming parameters, '
                                     'resource:{}, message:{},'.format(class_path, str(ex)))
        return access_control_cls


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        """
        {
            "app": "product",         # 注册的app名称
            "secret": "dlejlfekelme", # 注册的密钥
            "data": [
                {
                    "resource": "guide_admin",
                    "desc": "描述"
                },
                {
                    "resource": "shop_admin",
                    "desc": "专柜管理"
                }
            ]
        }
        ACCESS_CONTROL_REGISTER = {
            "ACCESS_CONTROL_SERVICE": {
                "ENV_NAME": "SPARROW_PERMISSION_HOST",
                # VALUE 为服务发现的注册名称
                "VALUE": os.environ.get("PERMISSION_SERVICE_SVC", "sparrow-permission-svc"),
            },
            "API_PATH": "",
            "SECRET": "",
            "ACCESS_CONTROL_CLASS": ""
        }

        """
        app_name = get_settings_value("SERVICE_CONF").get("NAME")
        api_path = get_settings_value("ACCESS_CONTROL").get("API_PATH")
        secret = get_settings_value("ACCESS_CONTROL").get("SECRET", None)
        service_conf = get_settings_value("ACCESS_CONTROL").get("ACCESS_CONTROL_SERVICE")
        access_control_class_path = get_settings_value("ACCESS_CONTROL").get("ACCESS_CONTROL_CLASS")
        if all([access_control_class_path, app_name, secret, service_conf]):
            access_control_cls = get_resource_cls(access_control_class_path)
            attribute_name_list = [_ for _ in dir(access_control_cls) if _.startswith('__') is False]
            data = [getattr(access_control_cls, _) for _ in attribute_name_list]
            try:
                rest_client.post(service_conf, api_path=api_path, json=data)
                print("resource register success!!!")
            except Exception as ex:
                print("resource register failed, message:{}".format(ex.__str__()))
