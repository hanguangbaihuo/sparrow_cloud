import json
from django.core.management.base import BaseCommand
from sparrow_cloud.apps.schema_command.schemas.generators import SchemaGenerator
from sparrow_cloud.apps.schema_command.contributor import get_git_contributors
from sparrow_cloud.apps.permission_command.management.commands._api import get_service_name
from django.conf import settings

from sparrow_cloud.restclient import rest_client
from sparrow_cloud.restclient.exception import HTTPException


class Command(BaseCommand):
    help = "注册api schema到文档中心"

    def add_arguments(self, parser):
        parser.add_argument(
            '-p', '--print',
            default=False, action="store_true",
            help='打印api schema 到控制台'
        )

    def handle(self, *args, **options):
        sg = SchemaGenerator()
        schema = sg.get_schema_dict()
        # print(schema)
        if not schema:
            return
        # 作者
        schema["contributors"] = get_git_contributors() or []
        # 服务名称
        schema["service_name"] = get_service_name()

        # 注册schema
        register(schema)
        if options["print"] is True:
            data = json.dumps(schema, ensure_ascii=False)
            print(data)


def register(schema):
    sparrow_permission_register_conf = settings.SPARROW_SCHEMA_REGISTER_CONF
    api_path = sparrow_permission_register_conf['API_PATH']
    permission_service_conf = sparrow_permission_register_conf["SCHEMA_SERVICE"]
    try:
        r = rest_client.post(permission_service_conf, api_path, json=schema)
        print("schema 注册成功 resp body={}".format(r))
    except HTTPException as ex:
        print("schema 注册失败. message={} ".format(ex.detail))



