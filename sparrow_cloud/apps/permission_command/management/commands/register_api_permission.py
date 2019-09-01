import json
import logging
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.utils.module_loading import import_string
from rest_framework.settings import api_settings
from sparrow_cloud.restclient import rest_client
import requests
import traceback
from pprint import pprint

class Command(BaseCommand):
    help = '实时注册APIs到认证中心'

    def add_arguments(self, parser):
        parser.add_argument(
            'auth_centre', metavar='auth-centre',
            nargs='?',
            default='',
            type=str,
            help='认证中心提供的注册接口地址'
        )
        parser.add_argument(
            '-d', '--django', dest='dj_ver',
            default="2", choices=["1", "2"],
            help='指定django的版本，可选值为1或2。如果django版本>=1.11,请选择2'
        )

        parser.add_argument(
            '-l', '--local', dest='local',
            default="0", choices=["0","1"],
            help='指定是不是permission本地导入，换句话说就是可以直接访问到permission自己的数据库'
        )

    def get_api_name(self, _paths, path, _method):
        # 获得权限的名字，从description中取前60个字符
        _api = _paths[path][_method]
        _name = _api["description"]
        if len(_name) == 0:
            _name = _api["operationId"]
        else:
            _name = _name[0:60]
        return _name

    # def register(self, schema, auth_centre, local, upd):
    #     try:
    #         #print(schema)
    #         _not_local=not local
    #         if local:
    #             try:
    #                 from auth_api.repository import PermissionRepository
    #                 PermissionRepository.batch_by_schema(schema, upd)
    #             except Exception as e:
    #                 traceback.print_exc()
    #                 print("导入时发生错误")
    #                 _not_local=True

    #         if _not_local and auth_centre:
    #             r = requests.post(auth_centre, data={
    #                 "schema": json.dumps(schema),
    #                 "upd": upd
    #             })
    #             if r.status_code == 200:
    #                 print("注册API成功")
    #             else:
    #                 print("注册API失败")
    #         else:
    #             if _not_local:
    #                print("未指定AUTH_CENTRE")
    #     except Exception as e:

    #         traceback.print_exc()
    #         print("issue")

    def register(self, api_list):
        permission_service_conf = settings.PERMISSION_SERVICE_CONF
        api_path = permission_service_conf.get("REGISTER_API")
        # import pdb; pdb.set_trace()
        try:
            rest_client.post(permission_service_conf, api_path, api_list)
        except Exception as ex:
            traceback.print_exc()

    def get_schema_generator(self, generator_class_name, api_name, api_version):
        generator_class = import_string(generator_class_name)
        return generator_class(
            name=api_name,
            version=api_version
        )

    def get_schema(self, generator, request, public):
        return generator.get_schema(request=request, public=public)

    def handle(self, auth_centre, dj_ver,local, *args, **kwargs):
        # disable logs of WARNING and below
        logging.disable(logging.WARNING)

        if dj_ver == "2":
            generator = self.get_schema_generator("sparrow_cloud.apps.permission_command.generators_django_2.OpenAPISchemaGenerator", "API",
                                                  "1.0")
        else:
            generator = self.get_schema_generator("sparrow_cloud.apps.permission_command.generators_django_1.SchemaGenerator", "API",
                                                  "1.0")
        schema = self.get_schema(generator, None, True)

        service_conf = settings.SERVICE_CONFIG
        service_name = service_conf.get("NAME")
        resutl = {
            "service_name": service_name,
            "api_list": schema
        }
        pprint(resutl)
        # 注册/更新 api 权限
        self.register(resutl)
        # for xx in schema:
            # if xx['is_regex']:
            # pprint(xx)
        # if not auth_centre:
        #     auth_centre=settings.AUTH_CENTRE
        # if local=="0":
        #     _local=False
        # else:
        #     _local=True
        # self.register(schema, auth_centre, local=_local,upd=True)

